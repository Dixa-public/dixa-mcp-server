"""Get a single conversation by ID from Dixa"""
from tools.utils import make_request


def get_conversation(conversation_id: str, log=None) -> str:
    """
    Get a single conversation by ID from Dixa.
    
    Args:
        conversation_id: The ID of the conversation to fetch
        log: Optional logger for debugging
    
    Returns:
        JSON string of the conversation data
    """
    url = f"https://dev.dixa.io/v1/conversations/{conversation_id}"
    data = make_request("GET", url, log=log)
    return data

