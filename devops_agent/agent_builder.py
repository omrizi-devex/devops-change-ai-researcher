# Ollama Integration
from langchain_community.chat_models import ChatOllama
from langchain.tools import BaseTool
from langchain_core.tools import BaseTool as CoreBaseTool

# FastMCP Adapter Components
from langchain_mcp_adapters.client import MultiServerMCPClient

# langgraph deep agent
from deepagents import create_deep_agent

# from state import AgentState


class DebugToolWrapper:
    """Wrapper around a tool that adds debugging output."""

    def __init__(self, wrapped_tool: BaseTool):
        self.wrapped_tool = wrapped_tool
        # Copy important attributes
        self.name = wrapped_tool.name
        self.description = wrapped_tool.description
        if hasattr(wrapped_tool, "args_schema"):
            self.args_schema = wrapped_tool.args_schema

    def __getattr__(self, name):
        # Delegate all other attributes to wrapped tool
        return getattr(self.wrapped_tool, name)

    async def arun(self, input_data, config=None, **kwargs):
        print(f"\n🔧 DEBUG: Tool '{self.wrapped_tool.name}' called")
        print(f"   Input type: {type(input_data)}")
        print(f"   Input value: {input_data}")
        if isinstance(input_data, dict):
            print(f"   Input keys: {list(input_data.keys())}")
            for key, value in input_data.items():
                print(f"     {key}: {value} (type: {type(value).__name__})")
        try:
            result = await self.wrapped_tool.arun(input_data, config, **kwargs)
            print(f"   ✅ Success")
            return result
        except Exception as e:
            print(f"   ❌ Error: {type(e).__name__}: {e}")
            import traceback

            traceback.print_exc()
            raise


# The MultiServerMCPClient handles connecting to and loading tools from the MCP server(s)
# The client is typically used inside an 'async with' block to ensure proper shutdown.
async def load_mcp_tools(client_config):
    """Initializes the MCP client and retrieves tools."""
    # Use the client to manage the server connection and tool loading
    client = MultiServerMCPClient(client_config)
    mcp_tools = await client.get_tools()
    print(f"✅ Successfully loaded {len(mcp_tools)} tools from FastMCP server(s).")

    # Wrap tools to add debugging
    wrapped_tools = [DebugToolWrapper(tool) for tool in mcp_tools]

    return wrapped_tools, client


def create_deepagent(llm, tools: list[BaseTool], system_prompt: str):
    return create_deep_agent(model=llm, tools=tools, system_prompt=system_prompt)
