
from flow_agent_package.tools.skills.agent_skill import AgentSkill
from flow_agent_package.tools.contracts import MIRSkillConfiguration
from promptflow.entities import CustomConnection as LocalCustomConnection
from semantic_kernel.skill_definition import sk_function
import requests 
import urllib
import openai
import json
from azure.ai.ml import MLClient

from semantic_kernel.skill_definition import sk_function, sk_function_context_parameter
from semantic_kernel.orchestration.sk_context import SKContext

class MIRSkill(AgentSkill):

    def __init__(self, config: MIRSkillConfiguration, memory_manager, ml_client: MLClient):
        super().__init__(config, memory_manager)
        self.mir_connection_name = config.mir_connection
        self.input_config = config.input_config
        self.ml_client = ml_client
        self.output_path = config.output_path


    def to_function_definition(self):
        """Represent the skill as a function definition"""
        return {
            "name": self.name,
            "description": self.tool_description,
            "parameters":{
                "type": "object",
                "properties": self.input_config
            }
        }
    
    def get_input_descriptions(self):
        input_description = "The inputs to this tool, in order, are \n"
        for input_name, input_metadata in self.input_config.items():
            input_description += f"Input Name: {input_name}, Input Type: {input_metadata['type']}"
            if input_metadata.get("description"):
                input_description += f"Input Description: {input_metadata.get('description')}"
            input_description += "\n"
        # print(f"Tool input description for {self.flow_name}: {input_description}")
        return input_description

    def get_langchain_tool_description(self):    
        return self.tool_description + self.get_input_descriptions()


    def to_langchain_function(self):

        def run_str(query):
            result = self.execute(json.loads(query))
            return result
        return run_str
        
    def to_sk_function(self):
        """Represent the skill as a sk function"""
        @sk_function(
            description=self.tool_description,
            name=self.name
        )
        def sk_execute_func(query: str) -> str:
            result = self.execute(json.loads(query))
            return result
        return sk_execute_func

    def to_sk_function_dynamic(self):
        """Represent the skill as a sk function with dynamic input decorators"""
        # TODO: See if there is a way to have dynamic decorators based on flows inputs (can you add decorators after the fact?)
        def sk_execute_func(context: SKContext) -> str:
            
            input_names = list(self.flow_manager.input_config.keys())
            input_json = {}
            for name in input_names:
                if name == self.changed_input:
                    sk_name = "input"
                else:
                    sk_name = name
                
                input_json[name] = context[sk_name]
                
            
            print(input_json)
            result = self.execute(input_json)
            return result
        og_func = sk_execute_func
        input_used = False
        for input_name, input_metadata in self.flow_manager.input_config.items():
            if input_used:
                name = input_name
                description = input_metadata.get("description", "")
                context_decorator = sk_function_context_parameter(name=name, description=description)
                og_func = context_decorator(og_func)
            else:
                name = "input"
                description = input_metadata.get("description", input_name)
                main_wrap = sk_function(description=self.function_description, name=self.name, input_description=description)
                og_func = main_wrap(og_func)
                self.changed_input = input_name
                input_used = True

    def get_mir_connection(self):
        
        region = self.ml_client.workspaces.get().location
        credential = self.ml_client._credential

        token = credential.get_token('https://management.azure.com/.default').token
        
        url = f"https://{region}.api.azureml.ms/rp/workspaces/subscriptions/{self.ml_client.subscription_id}/resourcegroups/" + \
            f"{self.ml_client.resource_group_name}/providers/Microsoft.MachineLearningServices/workspaces/" + \
            f"{self.ml_client.workspace_name}/connections/{self.mir_connection_name}/listsecrets?api-version=2023-02-01-preview"
        
        headers = {
            'Authorization': f'Bearer {token}',
            'content-type': 'application/json'
        }
            
        connection_json = requests.post(url, headers=headers).json()
        print(f"Connection json: {connection_json}")
        properties = connection_json["properties"]
        # The connection should allegedly have all information as it was validated in actual skill tool
        if properties["category"] == "CustomKeys":
            
            configs = {}
            secrets = {}
            auth_type = properties["metadata"]["authType"]
            configs["authType"] = auth_type
            configs["target"] = properties["metadata"]["target"]
            deployment = properties["metadata"].get("deployment")

            if deployment:
                configs["deployment"] = deployment

            if auth_type == "key":
                secrets["key"] = properties["credentials"]["keys"]["key"]
            

            mir_connection = LocalCustomConnection(
                secrets=secrets,
                configs = configs,
                name=self.mir_connection_name,
            )
        else:
            raise Exception(f"Connection Type Unsupported by Agent: {properties['category']}")

        return mir_connection

    def parse_output(self, response):
        json_path = self.output_path.split(",")
        current = response
        for step in json_path:
            try:
                # Handle list index values
                idx = int(step)
            except ValueError:
                # Can't parse, assume key
                idx = step
            current = current[idx]

        # After traversing path, should have answer
        return current

            

    def execute(self, inputs) -> dict:


        mir_connection = self.get_mir_connection()

        target = mir_connection.configs.get("target")
        deployment = mir_connection.configs.get("deployment")
        headers = {"Content-Type": "application/json"}
        if deployment:
            headers["azureml-model-deployment"] = deployment
        if mir_connection.configs.get("authType") == "key":
            headers["Authorization"] = "Bearer " + mir_connection.secrets.get("key")
        else:
            # Get AzureML Token somehow
            raise Exception('PAT not supported yet!')
            # Use token in header
        
        # Validate inputs
        for input_name, value in inputs.items():
            if input_name not in self.input_config.keys():
                raise Exception(f"Incorrect inputs for MIR Tool given by LLM: {inputs}")

        body = str.encode(json.dumps(inputs))
        try:
            response = requests.post(target, data=inputs, headers=headers).json()
            print(response)
            return self.parse_output(response)
        except Exception as error:
            print("The request failed with exception " + str(error))
            raise
        
