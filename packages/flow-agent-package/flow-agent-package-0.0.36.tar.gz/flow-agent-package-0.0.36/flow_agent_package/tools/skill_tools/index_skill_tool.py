from promptflow import tool
# The inputs section will change based on the arguments of the tool function, after you save the code
# Adding type to arguments and return value will help the system show the types properly
# Please update the function name/signature per need
from flow_agent_package.tools.contracts import MLIndexSkillConfiguration

# TODO: Fix input name and tool name
@tool
def mlindex_skill(name: str, description: str, asset_path: str, system_prompt:str = None, return_direct: bool = True):
  #TODO: Validate system prompt/ return direct here to fail fast
  config = MLIndexSkillConfiguration(name=name, description=description, index_path=asset_path, return_direct=return_direct, system_prompt=system_prompt)
  return config