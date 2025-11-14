"""Get all messages for a specific conversation from Dixa"""
from tools.utils import make_request


def get_conversation_messages(conversation_id: str, log=None) -> str:
    """
    Get all messages for a specific conversation from Dixa.
    
    Args:
        conversation_id: The ID of the conversation to fetch messages for
        log: Optional logger for debugging
    
    Returns:
        JSON string of the messages data
    """
    url = f"https://dev.dixa.io/v1/conversations/{conversation_id}/messages"
    data = make_request("GET", url, log=log)
    return data

