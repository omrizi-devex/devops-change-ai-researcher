from langchain_openai import ChatOpenAI
from settings import Settings
from langchain_core.messages import HumanMessage
from deepagents.backends import FilesystemBackend
from deepagents import create_deep_agent, CompiledSubAgent
from datetime import datetime
from langchain.agents import create_agent
from langgraph.checkpoint.memory import MemorySaver

# local imports
from langchain.tools import tool
from agent_tools import get_web_url_by_query, fetch_web_content
import sys
from promots import (
    RESEARCHER_INSTRUCTIONS,
    RESEARCH_WORKFLOW_INSTRUCTIONS,
    SUBAGENT_DELEGATION_INSTRUCTIONS,
)

def main():
    # Get user input from terminal
    query = sys.argv[1] if len(sys.argv) > 1 else input("Enter your query: ")
    settings = Settings()

    memory = MemorySaver()

    llm_openai = ChatOpenAI(
        model="gpt-5-nano",
        api_key=settings.api_key.get_secret_value(),
        temperature=0,
        max_retries=10,
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
        system_prompt=RESEARCHER_INSTRUCTIONS.format(
            date=datetime.now().strftime("%Y-%m-%d")
        ),
        tools=[get_web_url_by_query, fetch_web_content],
    )
    research_sub_agent = CompiledSubAgent(
        name="research-agent",
        description="Delegate research to the sub-agent researcher. Only give this researcher one topic at a time.",
        runnable=research_sub_agent_graph,
    )

    search_agent = create_deep_agent(
        model=llm_openai,
        tools=[get_web_url_by_query, fetch_web_content],
        system_prompt=INSTRUCTIONS,
        subagents=[research_sub_agent],
        backend=FilesystemBackend(root_dir="./reports", virtual_mode=True),
        checkpointer=memory,
    )

    print("\n🤖 Agent processing query...")
    response = search_agent.invoke({"messages": [HumanMessage(content=query)]})


if __name__ == "__main__":
    main()
