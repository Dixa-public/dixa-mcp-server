"""Get all tags associated with a specific conversation from Dixa"""
from tools.utils import make_request


def get_conversation_tags(conversation_id: str, log=None) -> str:
    """
    Get all tags associated with a specific conversation from Dixa.
    
    Args:
        conversation_id: The ID of the conversation to fetch tags for
        log: Optional logger for debugging
    
    Returns:
        JSON string of the tags data
    """
    url = f"https://dev.dixa.io/v1/conversations/{conversation_id}/tags"
    data = make_request("GET", url, log=log)
    return data

