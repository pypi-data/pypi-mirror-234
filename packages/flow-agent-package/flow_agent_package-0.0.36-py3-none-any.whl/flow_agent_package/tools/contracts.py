from dataclasses import dataclass
from enum import Enum
from promptflow.connections import CustomConnection

@dataclass
class AgentSkillConfiguration:
    name: str
    description: str
    return_direct: bool

@dataclass
class FlowSkillConfiguration(AgentSkillConfiguration):
    flow_name: str


@dataclass
class MLIndexSkillConfiguration(AgentSkillConfiguration):
    index_path: str
    system_prompt: str

@dataclass
class MIRSkillConfiguration(AgentSkillConfiguration):
    mir_connection: str
    input_config: dict
    output_path: str


class ArbitrationMethod(Enum):
  LANGCHAIN = "Langchain Zero Shot Agent"
  OPENAI_FUNCTIONS = "OpenAI Functions"
  SEMANTIC_KERNEL = "Semantic Kernel Custom Orchestrator"
  SEMANTIC_KERNEL_PLANNER = "Semantic Kernel Action Planner"