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
