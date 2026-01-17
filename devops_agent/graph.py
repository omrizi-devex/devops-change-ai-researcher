"""
Graph factory for LangGraph CLI.
This module provides a graph function that can be used by LangGraph CLI.
"""

from langchain_ollama import ChatOllama
import deep_agent
from settings import Settings
import asyncio
from typing import Any


def graph() -> Any:
    """
    Factory function that creates and returns the deep agent graph.
    This function is called by LangGraph CLI to get the graph instance.
    """
    settings = Settings()
    llm = ChatOllama(model=settings.ollama_model)

    # Initialize MCP tools
    mcp_tools = []

    # Load MCP tools asynchronously
    async def _load_tools():
        try:
            tools, _ = await deep_agent.load_mcp_tools(settings.mcp_config)
            return tools
        except Exception as e:
            print(f"Warning: Could not load MCP tools: {e}")
            print("Graph will be created without MCP tools.")
            return []

    # Load tools
    try:
        mcp_tools = asyncio.run(_load_tools())
    except RuntimeError:
        # If event loop is already running, try alternative approach
        try:
            loop = asyncio.get_event_loop()
            if loop.is_running():
                # Can't use run_until_complete in running loop
                print(
                    "Warning: Event loop is already running. Creating graph without MCP tools."
                )
                mcp_tools = []
            else:
                mcp_tools = loop.run_until_complete(_load_tools())
        except Exception as e:
            print(f"Warning: Could not load MCP tools: {e}")
            mcp_tools = []

    # Create the graph asynchronously
    async def _create_graph():
        return await deep_agent.create_deepagent(
            llm=llm, tools=mcp_tools, system_prompt=settings.system_prompt
        )

    try:
        agent_graph = asyncio.run(_create_graph())
    except RuntimeError:
        # Fallback for already running event loop
        try:
            loop = asyncio.get_event_loop()
            agent_graph = loop.run_until_complete(_create_graph())
        except Exception as e:
            raise RuntimeError(f"Failed to create graph: {e}") from e

    return agent_graph
