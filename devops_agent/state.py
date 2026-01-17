from typing import TypedDict, Annotated, List
from langchain_core.messages import BaseMessage
import operator


class AgentState(TypedDict):
    """The state of the agent, containing the conversation history."""

    messages: Annotated[List[BaseMessage], operator.add]
