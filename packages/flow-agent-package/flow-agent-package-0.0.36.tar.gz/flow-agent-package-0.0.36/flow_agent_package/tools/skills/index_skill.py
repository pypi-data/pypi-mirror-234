
from flow_agent_package.tools.skills.agent_skill import AgentSkill
from flow_agent_package.tools.contracts import AgentSkillConfiguration, MLIndexSkillConfiguration
from azureml.rag.mlindex import MLIndex
from semantic_kernel.skill_definition import sk_function
from promptflow.connections import AzureOpenAIConnection
from langchain.chat_models import AzureChatOpenAI
from langchain.schema.document import Document
from typing import List
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

import openai
import json

class MLIndexSkill(AgentSkill):

    def __init__(self, config: MLIndexSkillConfiguration, memory_manager, llm_connection: AzureOpenAIConnection, deployment_name):
        super().__init__(config, memory_manager)
        self.asset_path = config.index_path
        self.ml_index = MLIndex(config.index_path)
        self.system_prompt = config.system_prompt
        self.llm_connection = llm_connection
        self.deployment_name = deployment_name

    def to_function_definition(self):
        """Represent the skill as a function definition"""
        return {
            "name": self.name,
            "description": self.tool_description,
            "parameters":{
                "type": "object",
                "properties": {
                    "question" : {
                        "type": "string"
                    }
                }
            }
        }
    
    def get_langchain_tool_description(self):
        return self.tool_description + "The inputs to this tool, in order, are\n" + "Input Name: question \nInput Type: string\n"


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
        @sk_function(
            description=self.tool_description,
            name=self.name,
            input_description="Question for the docs source"
        )
        def sk_execute_func(query: str) -> str:
            result = self.execute(json.loads(query))
            return result
        return sk_execute_func

    def execute(self, inputs) -> dict:
        """Execute the Skill"""
        print("Bazinga")
        print(f"Inputs: {inputs}")
        retreiver = self.ml_index.as_langchain_retriever()
        retreiver.search_kwargs["k"] = 2
        docs = retreiver.get_relevant_documents(inputs["question"], k=2)
        print(f"Num Docs Retrieved: {len(docs)}")
        # If system prompt is provided, actually call llm with info
        if self.system_prompt:
            post_process = False
            # convert docs to string
            doc_string = generate_prompt_context(docs)

            # Use prompt with LLM via langchain
            llm = AzureChatOpenAI(client=openai.ChatCompletion,
                            temperature=0, 
                            deployment_name=self.deployment_name,
                            model_name=self.deployment_name, 
                            openai_api_key=self.llm_connection.api_key,
                            openai_api_base=self.llm_connection.api_base,
                            openai_api_type=self.llm_connection.api_type,
                            openai_api_version=self.llm_connection.api_version)
            
            template = PromptTemplate(input_variables=["context", "question"], template=self.system_prompt)

            chain = LLMChain(llm=llm, prompt=template)

            answer = chain.run({ "question": inputs["question"], "context": doc_string})
            return answer
        else:
            return docs

        # Otherwise, return the docs


def generate_prompt_context(search_result: List[Document]) -> str:
    def format_doc(doc: dict):
        return f"Content: {doc['Content']}\nSource: {doc['Source']}"
    
    SOURCE_KEY = "source"
    URL_KEY = "url"
    
    retrieved_docs = []
    for entity in search_result:
        content  = entity.page_content or ""
        
        source = ""
        if entity.metadata is not None:
            if SOURCE_KEY in entity.metadata:
                if URL_KEY in entity.metadata[SOURCE_KEY]:
                    source = entity.metadata[SOURCE_KEY][URL_KEY] or ""
        
        retrieved_docs.append({
            "Content": content,
            "Source": source
        })
    doc_string = "\n\n".join([format_doc(doc) for doc in retrieved_docs])
    return doc_string