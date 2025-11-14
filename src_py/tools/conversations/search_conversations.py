"""Search conversations in Dixa"""
from typing import Optional
from tools.utils import make_request


def search_conversations(
    query: str,
    exact_match: bool = True,
    page_key: Optional[str] = None,
    page_limit: int = 50,
    log=None,
) -> str:
    """
    Search conversations in Dixa.
    
    Args:
        query: The search query string
        exact_match: Whether to perform exact matching (default: True)
        page_key: Pagination key for next page of results
        page_limit: Number of results per page (default: 50)
        log: Optional logger for debugging
    
    Returns:
        JSON string of the search results
    """
    params = {
        "query": query,
        "exactMatch": str(exact_match),
    }
    
    if page_key:
        params["pageKey"] = page_key
    if page_limit is not None:
        params["pageLimit"] = str(page_limit)
    
    url = "https://dev.dixa.io/v1/search/conversations"
    data = make_request("GET", url, params=params, log=log)
    return data

