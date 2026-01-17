from langchain_openai import ChatOpenAI
from settings import Settings
from langchain_core.messages import HumanMessage, SystemMessage
from deepagents.backends import FilesystemBackend
from deepagents import create_deep_agent, CompiledSubAgent
from datetime import datetime
from langchain.agents import create_agent
from langgraph.checkpoint.postgres import PostgresSaver
from langgraph.store.postgres import PostgresStore
import uuid

# local imports
from langchain.tools import tool
from agent_tools import (
    get_web_url_by_query,
    fetch_web_content,
    update_long_term_memory,
    search_long_term_memory,
)
import sys
from promots import (
    RESEARCHER_INSTRUCTIONS,
    RESEARCH_WORKFLOW_INSTRUCTIONS,
    SUBAGENT_DELEGATION_INSTRUCTIONS,
    MEMORY_AGENT_INSTRUCTIONS,
    MEMORT_SEARCHER_AGENT_INSTRUCTIONS,
)


def print_agent_trace(agent_response) -> None:
    print(f"\n🤖 Agent Response Trace")

    # Better response handling
    print("\n" + "=" * 60)
    print("AGENT RESPONSE:")
    print("=" * 60)

    # Print all messages to see the conversation flow
    for i, msg in enumerate(agent_response.get("messages", [])):
        print(f"\nMessage {i+1} ({type(msg).__name__}):")
        if hasattr(msg, "content"):
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


def print_agent_last_message(agent_response) -> None:
    if agent_response.get("messages"):
        last_msg = agent_response["messages"][-1]
        print("\n" + "=" * 60)
        print("LAST MESSAGE DETAILS:")
        print("=" * 60)
        print(f"Type: {type(last_msg).__name__}")
        print(
            f"Content: {last_msg.content if hasattr(last_msg, 'content') else last_msg}"
        )
        if hasattr(last_msg, "response_metadata"):
            print(f"Metadata: {last_msg.response_metadata}")


def main():

    settings = Settings()

    DB_URI = "postgresql://postgres:postgres@localhost:5432/postgres?sslmode=disable"

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

    memory_saver_agent_graph = create_agent(
        model=llm_openai,
        name="memory-agent",
        system_prompt=MEMORY_AGENT_INSTRUCTIONS,
        tools=[update_long_term_memory],
    )
    memory_saver_agent = CompiledSubAgent(
        name="memory-agent",
        description="Delegate memory storage tasks to save valuable user information for long-term memory. Use this to store personal details, preferences, or context that would be useful in future conversations.",
        runnable=memory_saver_agent_graph,
    )

    memory_searcher_agent_graph = create_agent(
        model=llm_openai,
        name="memory-searcher-agent",
        system_prompt=MEMORT_SEARCHER_AGENT_INSTRUCTIONS,
        tools=[search_long_term_memory],
    )
    memory_searcher_agent = CompiledSubAgent(
        name="memory-searcher-agent",
        description="Delegate long-term memory searches to retrieve valuable user information and preferences before the interaction with the user starts.",
        runnable=memory_searcher_agent_graph,
    )

    with (
        PostgresStore.from_conn_string(DB_URI) as store,
        PostgresSaver.from_conn_string(DB_URI) as checkpointer,
    ):
        try:
            checkpointer.setup()
            store.setup()
        except Exception as e:
            print(f"Error initializing the postgres db store or checkpointer: {e}")

        search_agent = create_deep_agent(
            model=llm_openai,
            tools=[get_web_url_by_query, fetch_web_content],
            system_prompt=INSTRUCTIONS,
            subagents=[research_sub_agent, memory_saver_agent, memory_searcher_agent],
            backend=FilesystemBackend(root_dir="./reports", virtual_mode=True),
            checkpointer=checkpointer,
            store=store,
        )

        # user_id is hard coded now
        # In the futuere, we will take it from SSO login users db.
        user_id = "omriki-2011"
        thread_id = str(uuid.uuid4())
        config = {"configurable": {"thread_id": thread_id, "user_id": user_id}}
        namespace = ("memories", user_id)

        while True:
            query = input("Enter your query (or 'exit' to quit): ")

            if query.lower() == "exit":
                break

            print("\n🤖 Agent processing query...")
            # Build the message
            response = search_agent.invoke(
                {
                    "messages": [
                        HumanMessage(content=f"user_id: {user_id}\n{query}"),
                    ]
                },
                config=config,
            )
            response_message = response.get("messages")[-1].content
            print(f"Agent response ✨\n{response_message}")


if __name__ == "__main__":
    main()
