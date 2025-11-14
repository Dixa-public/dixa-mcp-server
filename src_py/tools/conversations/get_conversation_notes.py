"""Get all internal notes for a specific conversation from Dixa"""
from tools.utils import make_request


def get_conversation_notes(conversation_id: str, log=None) -> str:
    """
    Get all internal notes for a specific conversation from Dixa.
    
    Args:
        conversation_id: The ID of the conversation to fetch notes for
        log: Optional logger for debugging
    
    Returns:
        JSON string of the notes data
    """
    url = f"https://dev.dixa.io/v1/conversations/{conversation_id}/notes"
    data = make_request("GET", url, log=log)
    return data

