import requests
import uuid
import json
import os
from pathlib import Path
import tempfile
from datetime import datetime

from azureml.core import Workspace
from azureml.core.authentication import TokenAuthentication

from azure.mgmt.storage import StorageManagementClient
from azure.storage.fileshare import ShareServiceClient
from azure.storage.fileshare import ShareDirectoryClient
from azure.identity import DefaultAzureCredential
from azure.ai.ml._artifacts._fileshare_storage_helper import recursive_download

from flow_agent_package.tools.utils import get_token_for_audience, wait_for_completion, custom_active_instance

from promptflow.contracts.run_mode import RunMode
from promptflow.runtime.contracts.runtime import SubmitFlowRequest
from promptflow.core.thread_local_singleton import ThreadLocalSingleton
from promptflow.runtime import PromptFlowRuntime
from promptflow.entities import AzureOpenAIConnection as LocalAzureOpenAIConnection
from promptflow import PFClient as LocalPFClient
from promptflow._utils.logger_utils import flow_logger, logger, LogContext, get_logger
from promptflow._internal import Tracer, RunTracker, FlowExecutionContext
from promptflow._sdk.operations._local_storage_operations import LoggerOperations
from promptflow._sdk._constants import PROMPT_FLOW_DIR_NAME


class SubFlowManager:

    def __init__(self, working_dir):
        self.working_dir = working_dir

    def __enter__(self):
        self.active_execution_context = FlowExecutionContext.active_instance()
        self.active_tracer = Tracer.active_instance()
        self.active_tracker = RunTracker.active_instance()
        self.active_log_context = LogContext.get_current()
        
        if self.active_execution_context:
            self.active_execution_context._deactivate_in_context()

        if self.active_tracer:
            self.active_tracer._deactivate_in_context()
        
        if self.active_tracker:
            self.active_tracker._deactivate_in_context()
        
    def __exit__(self, *args):
        if self.active_execution_context:
            self.active_execution_context._activate_in_context(force=True)

        if self.active_tracer:
            self.active_tracer._activate_in_context(force=True)
        
        if self.active_tracker:
            self.active_tracker._activate_in_context(force=True)
        
        sub_flow_log_path = os.path.join(self.working_dir, PROMPT_FLOW_DIR_NAME, "flow.log")
        self.active_log_context._set_log_path()
        try:
            with open(sub_flow_log_path, "r") as sub_log:
                sub_log_data = sub_log.read()

            print(f"Logs from sub flow:\n{sub_log_data}")
        except Exception as e:
            print(f"Unable to copy logs from sub-flow execution: {str(e)}")

        


class FlowManager:
    #TODO: Add logging
    def __init__(self, client, flow_name, subscription_id, resource_group, workspace_name):
        self.client = client
        # TODO: See if there is another way for local PF
        self.local_client = LocalPFClient()
        self.flow_name = flow_name
        self.subscription_id = subscription_id
        self.resource_group = resource_group
        self.workspace_name = workspace_name
        
        # Probably just make these set, not return
        self.flow_dto = self.get_flow_dto_from_name()
        self.flow_json = self.get_flow_json_from_dto()
        self.is_chat_flow = False
        self.init_inputs()
        self.init_output()
        if self.flow_dto.flow_definition_file_path:
            self.is_code_first = True
        else:
            self.is_code_first = False
    
    def get_flow_dto_from_name(self):
        # List all flows
        # TODO: once Flow Operations are better supported, call that layer instead
        all_flows = self.client._flows._service_caller.list_flows(self.subscription_id, self.resource_group, self.workspace_name)

        for flow in all_flows:
            if flow.flow_name == self.flow_name:
                resp = self.client._flows._service_caller.get_flow(self.subscription_id, self.resource_group, self.workspace_name, flow.flow_id, flow.experiment_id)
                return resp
        raise Exception(f"Flow {self.flow_name} does not exist in workspace {self.workspace_name}")
    
    def get_flow_json_from_dto(self):
        

        graph = self.flow_dto.flow.flow_graph.as_dict()
        batch_inputs = self.flow_dto.flow_run_settings.as_dict()["batch_inputs"]
            
        final_json = {
            "flowName": self.flow_dto.flow_name,
            "description": self.flow_dto.description,
            "flowId": self.flow_dto.flow_id,
            "flow": graph,
            "batch_inputs": batch_inputs,
        }

        return final_json

    def init_inputs(self):
        base_inputs = self.flow_json["flow"]["inputs"]
        input_config = {}
        for input_name, input_info in base_inputs.items():
            # Don't add chat history as input, it is added manually later
            if input_name == "chat_history":
                self.is_chat_flow = True
                continue
            
            input_type = input_info.get("type")
            # TODO: add back input checking - do we need this?
            if input_type == None:
                raise Exception(f"Input {input_name} for tool {self.name} does not have a type specified!")
            # elif input_type == "object"
            #   raise Exception(f"Input {input_name} for tool {self.name} has incompatible type: {input_type}")
            
            input_description = input_info.get("description")
            # if input_description == None:
            #   raise Exception(f"Input {input_name} for tool {self.name} does not have a description!")
            temp = {"type": input_type}
            if input_description:
                temp["description"] = input_description
            input_config[input_name] = temp
        self.input_config = input_config
  
    def get_input_descriptions(self):
        input_description = "The inputs to this tool, in order, are \n"
        for input_name, input_metadata in self.input_config.items():
            input_description += f"Input Name: {input_name}, Input Type: {input_metadata['type']}"
            if input_metadata.get("description"):
                input_description += f"Input Description: {input_metadata.get('description')}"
            input_description += "\n"
        # print(f"Tool input description for {self.flow_name}: {input_description}")
        return input_description

    def init_output(self):
        outputs = self.flow_json["flow"]["outputs"]
        if len(outputs.keys()) != 1:
            raise Exception("Skills used in agent must have only one output!")
        self.output = list(outputs.keys())[0]

    def execute_flow(self, inputs):
        if self.is_code_first:
            print("Executing Code First Flow")
            print(f"Inputs: {inputs}")
            return self.execute_yaml_flow(inputs)
        else:
            print("Executing Json Flow")
            print(f"Inputs: {inputs}")
            return self.execute_json_flow(inputs)

    def execute_yaml_flow(self, inputs):
        self.set_connection_info()

        with tempfile.TemporaryDirectory() as tmpdirname:
            print('created temporary directory', tmpdirname)
            download_start_time = datetime.now()
            self.download_all_flow_files(tmpdirname)
            print(f"Time to Download Files: {datetime.now() - download_start_time}")
            flow_path = os.path.join(tmpdirname, "flow.dag.yaml")
            # TODO: Here and in json, figure out better way to deal with inputs

            # TODO: Figure out local submission if possible
            print(f"Inputs for local test: {inputs}")
            test_start_time = datetime.now()

            with SubFlowManager(tmpdirname):
                base_run = self.local_client.test(flow=flow_path, inputs=inputs)


            print(f"Time to Execute Code Flow Locally: {datetime.now() - test_start_time}")
            return base_run[self.output]
                    
            # TODO: Wait based on timeout, not retry count
            # if isinstance(inputs, dict):
            #     new_inputs = [inputs]
            # else:
            #     raise Exception(f"Incorrect input format: {type(inputs)}")
            # input_path = os.path.join(tmpdirname, "data.jsonl")
            # with open(input_path, 'w') as f:
            #     f.write('\n'.join(map(json.dumps, new_inputs)))
            # base_run = self.client.run(flow=flow_path, data=input_path, runtime=self.flow_dto.flow_run_settings.as_dict()["runtime_name"])
            # wait_for_completion(base_run, 5)
            # return self.local_client.get_details(base_run)[f"outputs.{self.output}"][0]

    def execute_json_flow(self, inputs) -> str:
        flow_request = self.create_submit_flow_request(inputs, None,)
        # TODO: Remove this - maybe not needed if full move to code first        
        ThreadLocalSingleton._activate_in_context = custom_active_instance

        runtime: PromptFlowRuntime = PromptFlowRuntime.get_instance()
        start = datetime.now()
        old_setting = runtime.config.execution.execute_in_process
        runtime.config.execution.execute_in_process = False
        # with SubFlowManager():
        result = runtime.execute(flow_request)
        
        runtime.config.execution.execute_in_process = old_setting
        end = datetime.now()
        print(f"Result from JSON subflow: {result}")
        print(f"Time to Execute JSON Subflow: {end - start}")
        result = result["flow_runs"][0]["output"][self.output][0]
        return result

    def set_connection_info(self):
        connection_start_time = datetime.now()
        workspace = Workspace(subscription_id=self.subscription_id, resource_group=self.resource_group, workspace_name=self.workspace_name, auth= TokenAuthentication(get_token_for_audience))
        endpoint = workspace.service_context._get_endpoint('api')
        graph = self.flow_json["flow"]
        connections = []
        for node in graph["nodes"]:
            if node.get("connection"):
                connections.append(node.get("connection"))
            tool_name = node["tool"]
            for tool in graph["tools"]:
                if tool["name"] == tool_name:
                    for input_name, metadata in tool.get("inputs", {}).items():
                        if "connection" in metadata["type"][0].lower():
                            connections.append(node["inputs"][input_name])

            if node.get("inputs", {}).get("connection"):
                connections.append(node["inputs"]["connection"])
        connection_configs = {}
        token = get_token_for_audience(None)
        headers = {
            'Authorization': f'Bearer {token}',
            'content-type': 'application/json'
        }
        for connection_name in set(connections):
            # TODO: Find better way than by HTTP call - maybe add support for this in azure PF
            url = f"{endpoint}/rp/workspaces/subscriptions/{workspace.subscription_id}/resourcegroups/" + \
            f"{workspace.resource_group}/providers/Microsoft.MachineLearningServices/workspaces/" + \
            f"{workspace.name}/connections/{connection_name}/listsecrets?api-version=2023-02-01-preview"

            
            connection_json = requests.post(url, headers=headers).json()
            properties = connection_json["properties"]
            # TODO: Add different connection type support as well
            if properties["category"] == "AzureOpenAI":
                connection = LocalAzureOpenAIConnection(
                        name=connection_name,
                        api_key=properties["credentials"]["key"],
                        api_base=properties["target"],
                        api_type=properties["metadata"].get("ApiType"),
                        api_version=properties["metadata"].get("ApiVersion"),
                    )
                self.local_client.connections.create_or_update(connection)
                config = {
                    "type": "AzureOpenAIConnection",
                    "value": {
                        "api_key": properties["credentials"]["key"],
                        "api_base": properties["target"],
                        "api_type": "azure",
                        "api_version": "2023-03-15-preview"
                    }
                }
                connection_configs[connection_name] = config
            else:
                raise Exception(f"Connection Type Unsupported by Agent: {properties['category']}")
        
        self.flow_json["connections"]= connection_configs
        print(f"Time to Get Connections: {datetime.now() - connection_start_time}")
    
    def create_submit_flow_request(
        self,
        inputs,
        source_run_id=None,
    ) -> dict:
        """Refine the request to raw request dict"""
        if self.flow_json.get("connections") == None:
            self.set_connection_info()

        request = self.flow_json
        flow_run_id = str(uuid.uuid4())
        if not source_run_id:
            source_run_id = str(uuid.uuid4())
        variant_runs = request.get("variants_runs", {})
        if variant_runs:
            request["variants_runs"] = {v: f"{vid}_{flow_run_id}" for v, vid in variant_runs.items()}
        if request.get("eval_flow_run_id"):
            request["eval_flow_run_id"] = f"{request['eval_flow_run_id']}_{flow_run_id}"
        if "id" not in request["flow"]:
            request["flow"]["id"] = str(uuid.uuid4())
        # TDOD: Fix input stuff, same as above
        if isinstance(inputs, str):
            old_inputs = request["batch_inputs"]
            for key in old_inputs[0]:
                old_inputs[0][key] = inputs
            request["batch_inputs"] = old_inputs
        elif isinstance(inputs, dict):
            request["batch_inputs"] = [inputs]

        print(f"final inputs: {request['batch_inputs']}")
        request_json =  {
            "FlowId": request["flow"]["id"],
            "FlowRunId": flow_run_id,
            "SourceFlowRunId": source_run_id,
            "SubmissionData": json.dumps(request),
            "BatchDataInput": request.get("batch_data_input", {}),
        }
        return SubmitFlowRequest.deserialize(request_json)
    
    def download_all_flow_files(self, working_directory):
        ml_client = self.client._ml_client
        ds = ml_client.datastores.get("workspaceworkingdirectory", include_secrets=True)
        storage_url = f"https://{ds.account_name}.file.core.windows.net"
        file_definition_path = self.flow_dto.flow_definition_file_path
        print(f"File Definition Path: {file_definition_path}")
        absolute_path = Path(file_definition_path).parent
        file_service_client = ShareDirectoryClient(
            account_url=storage_url,
            credential=ds.credentials.account_key,
            share_name=ds.file_share_name,
            directory_path=str(absolute_path)
        )

        recursive_download(file_service_client, destination=working_directory, max_concurrency=1)
