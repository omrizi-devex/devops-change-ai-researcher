from langchain_openai import ChatOpenAI
from settings import Settings
from deepagents import create_deep_agent, CompiledSubAgent
from actions_toolkit import core
import sys
from datetime import datetime
from deepagents.backends import FilesystemBackend
from langchain.agents import create_agent

# local imports
from devops_agent import agent_builder
from agent_tools import (
    get_web_url_by_query,
    fetch_web_content,
    think_tool
)
from promots import(
    RESEARCHER_INSTRUCTIONS,
    RESEARCH_WORKFLOW_INSTRUCTIONS,
    SUBAGENT_DELEGATION_INSTRUCTIONS,
)

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


# Get user input from terminal
query = sys.argv[1] if len(sys.argv) > 1 else input("Enter your query: ")
settings = Settings()

llm_openai = ChatOpenAI(
    model="gpt-5-nano",
    api_key=settings.api_key.get_secret_value(),
    temperature=0,
    max_retries=10
)

# Combine orchestrator instructions (RESEARCHER_INSTRUCTIONS only for sub-agents)
INSTRUCTIONS = (
    RESEARCH_WORKFLOW_INSTRUCTIONS
    + "\n\n"
    + "=" * 80
    + "\n\n"
    + SUBAGENT_DELEGATION_INSTRUCTIONS.format(
        max_concurrent_research_units=5,
        max_researcher_iterations=5,
    )
)

# Create research sub-agent
research_sub_agent_graph = create_agent(
    model=llm_openai,
    name="research-agent",
    system_prompt=RESEARCHER_INSTRUCTIONS.format(date=datetime.now().strftime("%Y-%m-%d")),
    tools=[get_web_url_by_query, fetch_web_content],
)

research_sub_agent = CompiledSubAgent(
    name="research-agent",
    description="Delegate research to the sub-agent researcher. Only give this researcher one topic at a time.",
    runnable=research_sub_agent_graph
)

search_agent = create_deep_agent(
    model=llm_openai,
    name="devops-research-orchestrator",
    system_prompt=INSTRUCTIONS,
    tools=[fetch_web_content, think_tool],
    subagents=[research_sub_agent],
    backend=FilesystemBackend(root_dir=".", virtual_mode=True),
    
)
