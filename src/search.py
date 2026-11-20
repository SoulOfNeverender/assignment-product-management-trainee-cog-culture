import os
from tavily import TavilyClient


def get_tavily_key() -> str:
    return os.getenv("TAVILY_API_KEY", "")


def web_search(query: str, api_key: str) -> list[dict]:
    if not api_key:
        raise RuntimeError("Missing Tavily API key")
    client = TavilyClient(api_key=api_key)
    response = client.search(
        query=query,
        search_depth="advanced",
        max_results=6,
        include_answer=False,
    )
    return [
        {
            "title": item.get("title", ""),
            "url": item.get("url", ""),
            "content": item.get("content", ""),
        }
        for item in (response.get("results") or [])
        if item.get("url")
    ]
