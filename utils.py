from actions_toolkit import core


def print_agent_trace(agent_response) -> None:
    core.debug(f"\n🤖 Agent Response Trace")

    # Better response handling
    core.debug("\n" + "=" * 60)
    core.debug("AGENT RESPONSE:")
    core.debug("=" * 60)

    # Print all messages to see the conversation flow
    for i, msg in enumerate(agent_response.get("messages", [])):
        core.debug(f"\nMessage {i+1} ({type(msg).__name__}):")
        if hasattr(msg, "content"):
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
        core.info("\n" + "=" * 60)
        core.info("LAST MESSAGE DETAILS:")
        core.info("=" * 60)
        core.info(f"Type: {type(last_msg).__name__}")
        core.info(
            f"Content: {last_msg.content if hasattr(last_msg, 'content') else last_msg}"
        )
        if hasattr(last_msg, "response_metadata"):
            core.info(f"Metadata: {last_msg.response_metadata}")
