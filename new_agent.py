from langchain_community.document_loaders import WebBaseLoader
from langchain_core.tools import Tool

@Tool(name="Internet Search Loader", description="Loads content from a specified URL.")
def fetch_web_content(url: str, max_length: int = 100000) -> str:
    loader = WebBaseLoader(url)
    data = loader.load()

    content = ""
    for doc in data:
        content += doc.page_content.replace('\n', '') + "\n"

    return content[:max_length]