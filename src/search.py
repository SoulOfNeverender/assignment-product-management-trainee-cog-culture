import os
import requests


def get_tavily_key() -> str:
    return os.getenv("TAVILY_API_KEY", "")


def web_search(query: str, api_key: str) -> list[dict]:
    if not api_key:
        raise RuntimeError("Missing Tavily API key")
    response = requests.post(
        "https://api.tavily.com/search",
        json={
            "api_key": api_key,
            "query": query,
            "search_depth": "advanced",
            "max_results": 6,
            "include_answer": False,
        },
        timeout=(5, 25),
    )
    if response.status_code == 401:
        raise RuntimeError("Invalid Tavily API key")
    if response.status_code == 429:
        raise RuntimeError("Tavily rate limit or usage limit reached")
    response.raise_for_status()
    payload = response.json()
    return [
        {
            "title": item.get("title", ""),
            "url": item.get("url", ""),
            "content": item.get("content", ""),
        }
        for item in (payload.get("results") or [])
        if item.get("url")
    ]
