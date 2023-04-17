# Haystack Human In Loop Tool

Human in Loop tool for [haystack](https://github.com/deepset-ai/haystack) Agents.  Uses human guidance to refine queries and improve performance.


## Installation

- Python pip: ```python3 -m pip install haystack-human-tool``` . This package will attempt to install the dependencies (farm-haystack>=1.15.0, redis, haystack-memory, bleach)
- Python pip (skip dependency installation: Use  ```python3 -m pip install haystack-human-tool --no-deps```
- Using git: ```pip install git+https://github.com/rolandtannous/haystack-human-tool.git@main#egg=haystack-human-tool```


## Usage

To use the human in the loop tool in your agent, you need three core components:
- `haystack-memory`: This is the memory library for haystack agents. It provides access to working and sensory memories.
- `HumanInLoopNode`: This node adds human in the loop to the agent as a tool. It allows the agent to seek guidance from the human user in order to refine the user query.
- `sensory-memory`: This is an in-memory implementation that mimics a human's brief sensory memory, lasting only for the duration of one interaction.

```py
from haystack.agents import Agent, Tool
from haystack.nodes import PromptNode
from haystack_memory.memory import MemoryRecallNode
from haystack_memory.utils import MemoryUtils
from haystack_human_tool.humaninloop import HumanInLoopNode
from haystack_human_tool.prompt_templates import agent_template

# Initialize the memory and the memory tool so the agent can retrieve the memory
sensory_memory = []
working_memory = []
memory_node = MemoryRecallNode(memory=working_memory)
memory_tool = Tool(name="Memory",
                   pipeline_or_node=memory_node,
                   description="Your memory. Always access this tool first to remember what you have learned.")

human_node = HumanInLoopNode(sensory_memory=sensory_memory)
human_tool = Tool(name="Human",
                  pipeline_or_node=human_node,
                  description="Access this tool to refine your query. Ask the human to rephrase the question or to explain what or who the human is referring to. Use the human's answer to rephrase your query for use as input to other tools")

prompt_node = PromptNode(model_name_or_path="text-davinci-003", 
                         api_key="<YOUR_OPENAI_KEY>", 
                         max_length=1024,
                         stop_words=["Observation:"])
memory_agent = Agent(prompt_node=prompt_node, prompt_template=agent_template)
memory_agent.add_tool(memory_tool)
memory_agent.add_tool(human_tool)

# Initialize the utils to save the query and the answers to the memory
memory_utils = MemoryUtils(working_memory=working_memory, sensory_memory=sensory_memory, agent=memory_agent)
result = memory_utils.chat("<Your Question>")
```


## Example

An Example can be found in the `examples/` folder. It contains the usage for all memory types.
To open the example in colab, click on the following links:
- Human in Tool powered agent: [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/gravityml/haystack-human-tool/blob/main/examples/example_humanloop_with_memory.ipynb)








