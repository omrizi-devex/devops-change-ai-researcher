from typing import List, Dict
from langchain_community.document_loaders import WebBaseLoader
from langchain.tools import tool
from langchain_community.tools import DuckDuckGoSearchResults

@tool("get_web_urls")
def get_web_url_by_query(query: str) -> List[Dict[str, str]]:
    """
    Uses DuckDuckGo to get web URLs based on a search query.
    Inputs:
        query: The search query string.
    Outputs:
        A list of dictionaries containing 'title', 'link', and 'snippet' for each search result.
    """
    DDG_TOOL = DuckDuckGoSearchResults(output_format='list')
    try:
        search_results = DDG_TOOL.run(query)
    except Exception as e:
        print(f"Error fetching search results: {e}")
        return [
            {"title": "Error",
             "link": "N/A",
             "snippet": "An error occurred while fetching search results."}
        ]
    if not search_results:
        return [
            {"title": "No Results",
             "link": "N/A",
             "snippet": "No search results found for the given query."}
        ]
    return search_results

@tool("fetch_web_content")
def fetch_web_content(url: str, max_length: int = 100000) -> str:
    """
    Fetches and returns the content of a web page given its URL.

    Inputs:
        url: The URL of the web page to fetch.
        max_length: The maximum length of the content to return.
    Outputs:
        The content of the web pages.
    """
    loader = WebBaseLoader(url)
    data = loader.load()

    content = ""
    for doc in data:
        content += doc.page_content.replace('\n', '') + "\n"

    return content[:max_length]

@tool(parse_docstring=True)
def think_tool(reflection: str) -> str:
    """Tool for strategic reflection on research progress and decision-making.

    Use this tool after each search to analyze results and plan next steps systematically.
    This creates a deliberate pause in the research workflow for quality decision-making.

    When to use:
    - After receiving search results: What key information did I find?
    - Before deciding next steps: Do I have enough to answer comprehensively?
    - When assessing research gaps: What specific information am I still missing?
    - Before concluding research: Can I provide a complete answer now?

    Reflection should address:
    1. Analysis of current findings - What concrete information have I gathered?
    2. Gap assessment - What crucial information is still missing?
    3. Quality evaluation - Do I have sufficient evidence/examples for a good answer?
    4. Strategic decision - Should I continue searching or provide my answer?

    Args:
        reflection: Your detailed reflection on research progress, findings, gaps, and next steps

    Returns:
        Confirmation that reflection was recorded for decision-making
    """
    return f"Reflection recorded: {reflection}"