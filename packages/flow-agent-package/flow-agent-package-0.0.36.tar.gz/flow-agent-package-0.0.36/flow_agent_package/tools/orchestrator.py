import json

from semantic_kernel import Kernel
from semantic_kernel.skill_definition import (
    sk_function,
)
from semantic_kernel.orchestration.sk_context import SKContext
from flow_agent_package.tools.constants import extract_input

class OrchestratorPlugin:
  def __init__(self, kernel: Kernel, skill_mapping):
      self._kernel = kernel
      self.skill_mapping = skill_mapping

  @sk_function(
      description="Routes the request to the appropriate function",
      name="route_request",
  )
  async def RouteRequest(self, context: SKContext) -> str:
      #TODO: Logging
      # Save the original user request
      print("Routing Request")
      request = context["input"]
      try:
        history = context["history"]
      except:
        history = ""
      native_funcs = self._kernel.skills.get_functions_view().native_functions["FlowPlugin"]
      func_options = [function.name for function in native_funcs]
      print(f"Functions returned {func_options}")
      # Add the list of available functions to the context
      # TODO: Potentially try out adding descriptions as well
      context["options"] = " ,".join(func_options)
        
      # Retrieve the intent from the user request
      GetIntent = self._kernel.skills.get_function("OrchestratorPlugin", "GetIntent")
      FormatResponse = self._kernel.skills.get_function(
          "OrchestratorPlugin", "FormatResponse"
      )
      
      self._kernel.create_semantic_function(
        extract_input,
        description="Takes a question and using chat history figures out input for a plugin",
        function_name="ExtractInputs",
        skill_name="OrchestratorPlugin"
      )

      await GetIntent.invoke_async(context=context)
      intent = context["input"].strip()
      
      print(f"context: {intent}")
      print(f"History: {history}")
      
      picked_function = self._kernel.skills.get_function("FlowPlugin", intent)

      # Create a new context object with the original request
      pipelineContext = self._kernel.create_new_context()
      pipelineContext["original_request"] = request
      pipelineContext["input"] = request
      pipelineContext["tool_name"] = intent
      pipelineContext["tool_input_description"] = self.skill_mapping[intent].flow_manager.get_input_descriptions()
      pipelineContext["history"] = history

      # TODO: Add ability to format response
      ExtractInputs = self._kernel.skills.get_function(
        "OrchestratorPlugin", "ExtractInputs"
      )
      if self.skill_mapping[intent].return_direct:
        output = await self._kernel.run_async(
          ExtractInputs,
          picked_function,
          input_context=pipelineContext,
        )      
      else:
        output = await self._kernel.run_async(
          ExtractInputs,
          picked_function,
          FormatResponse,
          input_context=pipelineContext,
        )    
      # TODO: Better memory management here
      # if len(history) != 0:
      #   print("Using History")
        
      #   pipelineContext["history"] = history
      #   ExtractInputs = self._kernel.skills.get_function(
      #       "OrchestratorPlugin", "ExtractInputs"
      #   )
      #   ExtractQueryFromJson = self._kernel.skills.get_function(
      #     "OrchestratorPlugin", "ExtractQueryFromJson"
      #   )
      #   if self.return_direct_mapping.get(intent):
      #     # Run the functions in a pipeline
      #     output = await self._kernel.run_async(
      #         ExtractInputs,
      #         ExtractQueryFromJson,
      #         picked_function,
      #         input_context=pipelineContext,
      #     )
      #   else:
      #     output = await self._kernel.run_async(
      #       ExtractInputs,
      #       ExtractQueryFromJson,
      #       picked_function,
      #       FormatResponse,
      #       input_context=pipelineContext,
      #     )
      # else:
      #   # Run the functions in a pipeline
      #   if self.return_direct_mapping.get(intent):
      #     output = await self._kernel.run_async(
      #         picked_function,
      #         input_context=pipelineContext,
      #     )
      #   else:
      #      output = await self._kernel.run_async(
      #         picked_function,
      #         FormatResponse,
      #         input_context=pipelineContext,
      #     )
      print(f"Final output: {output}")
      return output["input"]
  
  @sk_function(
    description="Extracts query from JSON",
    name="ExtractQueryFromJson",
  )
  def ExtractQueryFromJson(self, context: SKContext):
      query_json = json.loads(context["input"])

      context["input"] = query_json["query"]
      print(f"Extracted Input: {query_json['query']}")

      return context
