from langchain_ollama import ChatOllama
from settings import Settings
from fastmcp import Client
import asyncio
from langchain_core.messages import HumanMessage
from deepagents import create_deep_agent
from langgraph.graph import StateGraph, END
from typing import TypedDict
from langchain_core.messages import BaseMessage, AIMessage


# local imports
from devops_agent import agent_builder

async def main():
    settings = Settings()
    # Configure Ollama with explicit context window settings
    llm = ChatOllama(
        model=settings.ollama_model,
        num_ctx=8192,  # Increase context window
        temperature=0.7,
    )
    mcp_tools=[]
    mcp_client = None
    try:
        mcp_tools, mcp_client = await agent_builder.load_mcp_tools(settings.mcp_config)
        print(f"Loaded {len(mcp_tools)} MCP tools")
        for tool in mcp_tools:
            print(f"  - {tool.name}: {tool.description[:100]}...")
    except Exception as e:
        print(f"Error: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()
    
    
    user_query = input("Enter your query: ")

    search_agent = agent_builder.create_deepagent(
        llm=llm,
        tools=mcp_tools,
        system_prompt=settings.system_prompt
    )

    print("\n🤖 Agent processing query...")
    response = await search_agent.ainvoke({"messages": [HumanMessage(content=user_query)]})
    
    # Better response handling
    print("\n" + "="*60)
    print("AGENT RESPONSE:")
    print("="*60)
    
    # Print all messages to see the conversation flow
    for i, msg in enumerate(response.get("messages", [])):
        print(f"\nMessage {i+1} ({type(msg).__name__}):")
        if hasattr(msg, 'content'):
            content = msg.content
            if isinstance(content, str):
                print(content)
            elif isinstance(content, list):
                for item in content:
                    print(f"  {item}")
            else:
                print(f"  {content}")
        else:
            print(f"  {msg}")
    
    # Print the last message in detail
    if response.get("messages"):
        last_msg = response["messages"][-1]
        print("\n" + "="*60)
        print("LAST MESSAGE DETAILS:")
        print("="*60)
        print(f"Type: {type(last_msg).__name__}")
        print(f"Content: {last_msg.content if hasattr(last_msg, 'content') else last_msg}")
        if hasattr(last_msg, 'response_metadata'):
            print(f"Metadata: {last_msg.response_metadata}")
    


if __name__ == "__main__":
    asyncio.run(main())
