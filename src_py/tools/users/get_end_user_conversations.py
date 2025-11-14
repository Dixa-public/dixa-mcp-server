"""Get all conversations for a specific end user from Dixa"""
from typing import Optional
from tools.utils import make_request


def get_end_user_conversations(
    user_id: str,
    page_key: Optional[str] = None,
    page_limit: int = 50,
    log=None,
) -> str:
    """
    Get all conversations for a specific end user from Dixa.
    
    Args:
        user_id: The ID of the end user to fetch conversations for
        page_key: Pagination key for next page of results
        page_limit: Number of results per page (default: 50)
        log: Optional logger for debugging
    
    Returns:
        JSON string of the conversations data
    """
    params = {}
    
    if page_key:
        params["pageKey"] = page_key
    if page_limit is not None:
        params["pageLimit"] = str(page_limit)
    
    url = f"https://dev.dixa.io/v1/endusers/{user_id}/conversations"
    data = make_request("GET", url, params=params, log=log)
    return data

