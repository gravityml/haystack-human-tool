# import component  BaseComponent from haystack nodes library
from abc import ABC
from typing import Optional, List
from haystack_memory.utils import MemoryUtils
import bleach
from bleach import clean

from haystack.nodes.base import BaseComponent


# declare class HumanInLoopNode with BaseComponent as parent class
class HumanInLoopNode(BaseComponent, ABC):
    """
    HumanInLoopNode is a component that allows you to manually review the results of a query and decide whether to
    continue the search or not. It can be used as a component in a pipeline or as a standalone tool.
    """

    # define the number of outgoing edges
    outgoing_edges = 1

    # define the init function
    def __init__(self, sensory_memory: List[str], **kwargs):
        """
        :param kwargs: Additional kwargs to be passed to BaseComponent
        """
        # call the init function of the parent class
        super(HumanInLoopNode, self).__init__(**kwargs)
        self.sensory_memory = sensory_memory

    # initialize sensory memory
    def __initialize_sensory_memory(self):
        self.sensory_memory.clear()

    # define the prompt function
    def __prompt_function(self, query: Optional[str] = " \n") -> None:
        self.sensory_memory.append(query)
        print(query)

    # Ask user for input
    def __input_function(self) -> str:
        human_input = input()
        self.sensory_memory.append(human_input)
        return bleach.clean(human_input)

    # define the run function
    def run(self, query: Optional[str] = "\n", **kwargs):
        """
        :param query:
        :param kwargs: Additional kwargs to be passed to BaseComponent
        :return: The input to the component
        """
        # initialize the sensory memory
        self.__initialize_sensory_memory()

        # call the prompt function
        self.__prompt_function(query)

        # call the input function
        user_answer = self.__input_function()

        # return user input to Agent
        return user_answer

    # define the run_batch function
    def run_batch(
            self,
            **kwargs
    ):
        pass
