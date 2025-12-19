from langchain_openai import ChatOpenAI
from settings import Settings
from langchain_core.messages import HumanMessage
from deepagents import create_deep_agent
from langchain_core.messages import BaseMessage, AIMessage
from actions_toolkit import core

# local imports
from devops_agent import agent_builder
from langchain.tools import tool
from agent_tools import get_web_url_by_query, fetch_web_content
import sys

def print_agent_trace(agent_response) -> None:
    core.debug(f"\n🤖 Agent Response Trace")

    # Better response handling
    core.debug("\n" + "="*60)
    core.debug("AGENT RESPONSE:")
    core.debug("="*60)
    
    # Print all messages to see the conversation flow
    for i, msg in enumerate(agent_response.get("messages", [])):
        core.debug(f"\nMessage {i+1} ({type(msg).__name__}):")
        if hasattr(msg, 'content'):
            content = msg.content
            if isinstance(content, str):
                core.debug(content)
            elif isinstance(content, list):
                for item in content:
                    core.debug(f"  {item}")
            else:
                core.debug(f"  {content}")
        else:
            core.debug(f"  {msg}")

def print_agent_last_message(agent_response) -> None:    
    if agent_response.get("messages"):
        last_msg = agent_response["messages"][-1]
        core.info("\n" + "="*60)
        core.info("LAST MESSAGE DETAILS:")
        core.info("="*60)
        core.info(f"Type: {type(last_msg).__name__}")
        core.info(f"Content: {last_msg.content if hasattr(last_msg, 'content') else last_msg}")
        if hasattr(last_msg, 'response_metadata'):
            core.info(f"Metadata: {last_msg.response_metadata}")


def main():
    # Get user input from terminal
    query = sys.argv[1] if len(sys.argv) > 1 else input("Enter your query: ")
    settings = Settings()

    llm_openai = ChatOpenAI(
        model="gpt-5-nano",
        api_key=settings.api_key.get_secret_value(),
        temperature=0,
        max_retries=10
    )

    search_agent = agent_builder.create_deepagent(
        llm=llm_openai,
        tools=[get_web_url_by_query, fetch_web_content],
        system_prompt=settings.kubernetes_system_prompt
    )
    
    print("\n🤖 Agent processing query...")
    response = search_agent.invoke({"messages": [HumanMessage(content=query)]})

    if settings.runner_debug == "1":
        print_agent_trace(response)
    
    print_agent_last_message(response)

if __name__ == "__main__":
    main()
