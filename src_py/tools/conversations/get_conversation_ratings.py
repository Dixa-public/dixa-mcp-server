"""Get all ratings for a specific conversation from Dixa"""
from tools.utils import make_request


def get_conversation_ratings(conversation_id: str, log=None) -> str:
    """
    Get all ratings for a specific conversation from Dixa.
    
    Args:
        conversation_id: The ID of the conversation to fetch ratings for
        log: Optional logger for debugging
    
    Returns:
        JSON string of the ratings data
    """
    url = f"https://dev.dixa.io/v1/conversations/{conversation_id}/ratings"
    data = make_request("GET", url, log=log)
    return data

