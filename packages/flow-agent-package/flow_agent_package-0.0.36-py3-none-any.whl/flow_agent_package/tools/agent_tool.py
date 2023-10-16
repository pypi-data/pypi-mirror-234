import json
import openai
from datetime import datetime


from promptflow import tool
from promptflow.runtime import PromptFlowRuntime
from promptflow.connections import AzureOpenAIConnection
from promptflow.entities import AzureOpenAIConnection as LocalAzureOpenAIConnection
from promptflow.azure import PFClient

from langchain.agents import Tool, AgentType, initialize_agent
from langchain.chat_models import AzureChatOpenAI
from langchain.chat_models import AzureChatOpenAI


import semantic_kernel as sk
from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion
from semantic_kernel.orchestration.context_variables import ContextVariables
from semantic_kernel.planning.basic_planner import BasicPlanner
from semantic_kernel.planning import ActionPlanner

from azure.identity import DefaultAzureCredential
from azure.ai.ml import MLClient

from flow_agent_package.tools.contracts import AgentSkillConfiguration, MLIndexSkillConfiguration, FlowSkillConfiguration, ArbitrationMethod, MIRSkillConfiguration
from flow_agent_package.tools.constants import format_response, intent_prompt, intent_prompt_with_history, extract_input, format_instructions_conversation, format_instructions_zero, planner_with_history
from flow_agent_package.tools.orchestrator import OrchestratorPlugin
from flow_agent_package.tools.memory import MemoryHelper
from flow_agent_package.tools.skills.agent_skill import AgentSkill
from flow_agent_package.tools.skills.flow_skill import FlowSkill
from flow_agent_package.tools.skills.index_skill import MLIndexSkill
from flow_agent_package.tools.skills.mir_skill import MIRSkill


class ArbitrationAgent:

  def __init__(self, arbitration_method, agent_connection, deployment_name, skills, memory_manager):
    self.arbitration_method = arbitration_method
    self.agent_connection = agent_connection
    self.skills = skills
    self.deployment_name = deployment_name
    self.memory_helper = memory_manager

    # TODO: Confirm if old api version works
    openai.api_base = agent_connection.api_base
    openai.api_type = agent_connection.api_type
    openai.api_version = "2023-07-01-preview"
    openai.api_key = agent_connection.api_key

  def execute(self, query):
    if self.arbitration_method == ArbitrationMethod.LANGCHAIN.value:
      return self.use_langchain(query)
    elif self.arbitration_method == ArbitrationMethod.OPENAI_FUNCTIONS.value:
      return self.use_openai_functions(query)
    elif self.arbitration_method == ArbitrationMethod.SEMANTIC_KERNEL.value:
      return self.use_semantic_kernel(query)
    elif self.arbitration_method == ArbitrationMethod.SEMANTIC_KERNEL_PLANNER.value:
      import asyncio
      return asyncio.run(self.use_semantic_planner(query))
    else:
      raise Exception(f"Invalid arbitration method used: {self.arbitration_method}")
  
  # TODO: Add better error handling to everything
  def use_langchain(self, query):
    print("Using Langchain Arbitration")
    tools = []
    for skill in self.skills:
      run_func = skill.to_langchain_function()
      lang_tool = Tool(
        name=skill.name,
        func=run_func,
        description=skill.get_langchain_tool_description(), #TODO: Potentially use openai function desc - check with Prakhar
        return_direct=skill.return_direct
      )
      tools.append(lang_tool)
    print("Added skills")
    # TODO: parameterize temperature? - how to get LLM interface like other tools?
    llm = AzureChatOpenAI(client=openai.ChatCompletion,
                            temperature=0, 
                            deployment_name=self.deployment_name,
                            model_name=self.deployment_name, 
                            openai_api_key=self.agent_connection.api_key,
                            openai_api_base=self.agent_connection.api_base,
                            openai_api_type=self.agent_connection.api_type,
                            openai_api_version=self.agent_connection.api_version)
    
    if self.memory_helper.use_history():
      # print("Using memory")
      memory = self.memory_helper.as_langchain_memory()
      # print(f"Memory: {memory}")
      agent_type = AgentType.CONVERSATIONAL_REACT_DESCRIPTION
      agent = initialize_agent(
              tools,
              llm,
              agent_kwargs= {"format_instructions": format_instructions_conversation},
              agent=agent_type,
              memory=memory,
              verbose=True)
    else:
      agent_type = AgentType.ZERO_SHOT_REACT_DESCRIPTION
      agent = initialize_agent(
              tools,
              llm,
              agent_kwargs= {"format_instructions": format_instructions_zero},
              agent=agent_type,
              verbose=True)
    print("Asking Langchain Agent Question")
    answer = agent.run(query)
    return answer

  def use_openai_functions(self, query):
    # Call OpenAI to pick function
    print("Using OpenAI Functions Arbitration")
    functions = []
    function_names_mapping = {}
    for skill in self.skills:
      func_def = skill.to_function_definition()
      functions.append(func_def)
      function_names_mapping[func_def["name"]] = skill

    messages = [
      {
        "role": "system",
        "content": "Assistant is a helpful assistant that is good at using provided functions to get answers to specific questions. You must pick a function as a response"
      },
    ]

    if self.memory_helper.use_history():
      print("Using memory")
      messages.extend(self.memory_helper.as_openai_function_memory())

    messages.append(
      {
        "role": "user",
        "content": query
      }
    )

    print(f"Functions: {functions}")
    response = openai.ChatCompletion.create(
        deployment_id=self.deployment_name,
        messages=messages,
        functions=functions,
        function_call="auto", 
    )
    response_message = response["choices"][0]["message"]
    print(f"Response from OpenAI: {response_message}")
    # Call Function
    if response_message.get("function_call"):
        print("Recommended Function call:")
        print(response_message.get("function_call"))
        print()
        
        # Step 3: call the function
        # Note: the JSON response may not always be valid; be sure to handle errors
        
        function_name = response_message["function_call"]["name"]
        
        # verify function exists
        if function_name not in function_names_mapping:
            return "Function " + function_name + " does not exist"
        tool_to_use = function_names_mapping[function_name]  
        
        # verify function has correct number of arguments
        # TODO: Actually verify arguments and types 
        function_args = json.loads(response_message["function_call"]["arguments"])
        print(f"Function Args: {function_args}")
        flow_result = tool_to_use.execute(function_args)

        print("Output of function call:")
        print(flow_result)
        print()
        
        if tool_to_use.return_direct:
          return flow_result
        
        messages.append(
            {
                "role": response_message["role"],
                "name": response_message["function_call"]["name"],
                "content": response_message["function_call"]["arguments"],
            }
        )

        # adding function response to messages
        messages.append(
            {
                "role": "function",
                "name": function_name,
                "content": json.dumps(flow_result),
            }
        )  # extend conversation with function response

        print("Messages in next request:")
        for message in messages:
            print(message)
        print()
        response = openai.ChatCompletion.create(
            messages=messages,
            deployment_id=self.deployment_name,
            function_call="none",
            functions=functions,
            temperature=0
        )

        answer = response['choices'][0]['message']["content"]
    else:
      answer = response_message

    return answer

  async def use_semantic_planner(self, query):
    print("Using Semantic Kernel Planner")
    my_logger = sk.NullLogger()
    kernel = sk.Kernel(log=my_logger)
    kernel.add_text_completion_service("dv", AzureChatCompletion(self.deployment_name, self.agent_connection.api_base, self.agent_connection.api_key))

    native_funcs = {}
    skill_mapping = {}
    print(f"Loading skills as native functions")

    for skill in self.skills:
      native_funcs[skill.name] = skill.to_sk_function_dynamic()
      skill_mapping[skill.name] = skill
    kernel.import_skill(native_funcs, "FlowPlugin")
    if self.memory_helper.use_history():
      planner = ActionPlanner(kernel, planner_with_history)
      planner._context["history"] = self.memory_helper.as_semantic_kernel_memory()
    else:
      planner = ActionPlanner(kernel)
    plan = await planner.create_plan_async(goal=query)
    print(plan.describe())
    result = await plan.invoke_async()
    return result["input"]

  def use_semantic_kernel(self, query):
    print("Using Semantic Kernel Arbitration")
    my_logger = sk.NullLogger()
    kernel = sk.Kernel(log=my_logger)
    kernel.add_text_completion_service("dv", AzureChatCompletion(self.deployment_name, self.agent_connection.api_base, self.agent_connection.api_key))

    print(f"Loading semantic Functions")
    # TODO: Move semantic functions to folder like SK example

    kernel.create_semantic_function(
      format_response,
      description="Takes a question and answer and formats it in a human readable way",
      function_name="FormatResponse",
      skill_name="OrchestratorPlugin"
    )


    # For each tool, import the skills (can we do this?)

    native_funcs = {}
    skill_mapping = {}
    print(f"Loading skills as native functions")

    for skill in self.skills:
      native_funcs[skill.name] = skill.to_sk_function()
      skill_mapping[skill.name] = skill
    kernel.import_skill(native_funcs, "FlowPlugin")
    
    orchestratorPlugin = kernel.import_skill(
        OrchestratorPlugin(kernel, skill_mapping), "OrchestratorPlugin"
    )
    
    if self.memory_helper.use_history():
      print("Using Memory")
      context = ContextVariables()
      # Use history to get intent
      kernel.create_semantic_function(
        intent_prompt_with_history,
        description="Gets the intent of the user",
        function_name="GetIntent",
        skill_name="OrchestratorPlugin"
      )

      # Add function to get final input for tool
      context["history"] = self.memory_helper.as_semantic_kernel_memory()
      context["input"] = query
      print("Calling SK Orchestrator")
      result = orchestratorPlugin["route_request"].invoke(
          query, context
      )
    else:
      kernel.create_semantic_function(
        intent_prompt,
        description="Gets the intent of the user",
        function_name="GetIntent",
        skill_name="OrchestratorPlugin"
      )
      print("Calling SK Orchestrator")
      result = orchestratorPlugin["route_request"].invoke(
          query
      )

    print(f"This is result: {result}")
    answer = result["input"]
    return answer

@tool
def agent(
    query: str,
    chat_history: list,
    arbitration_method: ArbitrationMethod,
    llm_connection: AzureOpenAIConnection,
    deployment_name: str,
    skill_1: AgentSkillConfiguration = None,
    skill_2: AgentSkillConfiguration  = None,
    skill_3: AgentSkillConfiguration = None,
    skill_4: AgentSkillConfiguration = None,
    skill_5: AgentSkillConfiguration = None
):
  # TODO: List of skill support
  agent_start_time = datetime.now()
  print(f"Agent Start Time: {agent_start_time}")
  print(f"User Query: {query}")
  print(f"Arbitration Method: {arbitration_method}")
  print(f"Chat History: {chat_history}")
  
  # Hacky way to get subscription info so we can communicate with WS
  # TODO: Bad way to get subscription information
  deploy_config = PromptFlowRuntime.get_instance().config.deployment
  subscription_id = deploy_config.subscription_id
  resource_group_name=deploy_config.resource_group
  workspace_name=deploy_config.workspace_name

  subscription_id = deploy_config.subscription_id if deploy_config.subscription_id != "" else "381b38e9-9840-4719-a5a0-61d9585e1e91"
  resource_group_name=deploy_config.resource_group if deploy_config.resource_group != "" else "baker-static"
  workspace_name=deploy_config.workspace_name if deploy_config.workspace_name != "" else "baker-eastus2"
  # subscription_id = "381b38e9-9840-4719-a5a0-61d9585e1e91"
  # resource_group_name="baker-static"
  # workspace_name= "baker-eastus2"
  print("Creating ML and PF Client")
  credential = DefaultAzureCredential()
  ml_client = MLClient(
      credential=credential,
      subscription_id=subscription_id,  # this will look like xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
      resource_group_name=resource_group_name,
      workspace_name=workspace_name,
  )
  pf = PFClient(ml_client=ml_client)

  print(f"Workspace Details: {subscription_id}, {resource_group_name}, {workspace_name}")

  print(f"Creating memory manager")
  memory_manager = MemoryHelper(chat_history)
  agent_skills = []
  skill_configs = [skill_1, skill_2, skill_3, skill_4, skill_5]
  for config in skill_configs:
    if config:
      if isinstance(config, MLIndexSkillConfiguration):
        skill = MLIndexSkill(config, memory_manager, llm_connection, deployment_name)
      elif isinstance(config, MIRSkillConfiguration):
        skill = MIRSkill(config, memory_manager, ml_client)
      else:
        skill = FlowSkill(config, pf, subscription_id, resource_group_name, workspace_name, memory_manager)
      agent_skills.append(skill)
  
  if len(agent_skills) == 0:
    raise Exception("No Valid Skills Were Provided to Agent!")

  print(f"Number of Skills for Agent: {len(agent_skills)}")

  arbitration_agent = ArbitrationAgent(arbitration_method, llm_connection, deployment_name, agent_skills, memory_manager)
  answer = arbitration_agent.execute(query)
  print(f"Time to e2e Execute Agent: {datetime.now() - agent_start_time}")
  return answer
