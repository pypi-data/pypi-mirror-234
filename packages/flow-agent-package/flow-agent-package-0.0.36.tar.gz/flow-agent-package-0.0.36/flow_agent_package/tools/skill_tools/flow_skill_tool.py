from promptflow import tool
# The inputs section will change based on the arguments of the tool function, after you save the code
# Adding type to arguments and return value will help the system show the types properly
# Please update the function name/signature per need
from flow_agent_package.tools.contracts import FlowSkillConfiguration

# TODO: Fix input name and tool name
@tool
def flow_skill(name: str, description: str, flow_id: str, return_direct: bool):
  config = FlowSkillConfiguration(name=name, description=description, flow_name=flow_id, return_direct=return_direct)
  return config
