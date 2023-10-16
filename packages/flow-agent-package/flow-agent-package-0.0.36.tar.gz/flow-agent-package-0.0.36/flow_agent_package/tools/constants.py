# TODO: Move to separeate files like SK example
# Prompt for SK GetIntent function
intent_prompt = """
User: {{$input}}

---------------------------------------------

Provide the intent of the user. The intent should be one of the following: {{$options}}

INTENT: 
"""

# Prompt for SK GetIntent function, using history
intent_prompt_with_history = """
{{$history}}
User: {{$input}}

---------------------------------------------

Provide the intent of the user. The intent should be one of the following: {{$options}}

INTENT: 
"""

# Prompt to get input for skill
extract_input = """
{{$history}}
User: {{$input}}

---------------------------------------------

Provide the input that should be sent to the {{$tool_name}} tool by making use of the history. The following are the inputs for the tool:
{{$tool_input_description}}
The input for the action be a json object that pairs input names to the values you choose. For example, if input_a is 10 and input_b is "hi", then your response should be ```{ "input_a": 10, "input_b": "hi"}```
Values for inputs can also come from what the Bot has said

INPUT: 
"""

# Prompt to format the response nicely
format_response = """
The answer to the users request is: {{$input}}
The bot should provide the answer back to the user.

User: {{$original_request}}
Bot: 
"""

format_instructions_conversation = """To use a tool, please use the following format:

```
Thought: Do I need to use a tool? Yes
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action. The input should be a json object that pairs input names to the values you choose. For example, if input_a is 10 and input_b is "hi", then your response should be {{{{ "input_a": 10, "input_b": "hi"}}}}
Observation: the result of the action
```

When you have a response to say to the Human, or if you do not need to use a tool, you MUST use the format (the prefix of "Thought: " and "{ai_prefix}: " are must be included):
Make sure that your response fits the proper formatting.

```
Thought: Do I need to use a tool? No
{ai_prefix}: [your response here]
```"""


format_instructions_zero = """Use the following format:

Question: the input question you must answer
Thought: you should always think about what to do
Action: the action to take, should be one of [{tool_names}].
Action Input: the input to the action. The input for the action should be a json object that pairs input names to the values you choose. For example, if input_a is 10 and input_b is "hi", then your response should be {{{{ "input_a": 10, "input_b": "hi"}}}}
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: the final answer to the original input question"""


planner_with_history = """
A planner takes a list of functions, chat history, a goal, and chooses which function to use.
For each function the list includes details about the input parameters.
[START OF EXAMPLES]
{{this.GoodExamples}}
{{this.EdgeCaseExamples}}
[END OF EXAMPLES]
[REAL SCENARIO STARTS HERE]
- List of functions:
{{this.ListOfFunctions}}
- End list of functions.
- Chat History Starts:
{{ $history }}
- Chat History Ends

Goal: {{ $input }}

"""

answer_with_documents_prompt = """
system: 
You are an AI assistant that helps users answer questions given a specific context. You will be given a context, and then asked a question based on that context. Your answer should be as precise as possible, and should only come from the context.
Please add citation after each sentence when possible in a form "(Source: citation)".

 user: 
 {{contexts}} 
 Human: {{question}} 
AI:
"""