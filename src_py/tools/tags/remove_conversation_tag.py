"""Remove a tag from a specific conversation in Dixa"""
from tools.utils import make_request


def remove_conversation_tag(conversation_id: str, tag_id: str, log=None) -> str:
    """
    Remove a tag from a specific conversation in Dixa.
    
    Args:
        conversation_id: The ID of the conversation to remove the tag from
        tag_id: The ID of the tag to remove from the conversation
        log: Optional logger for debugging
    
    Returns:
        JSON string indicating success or error
    """
    url = f"https://dev.dixa.io/v1/conversations/{conversation_id}/tags/{tag_id}"
    data = make_request("DELETE", url, log=log)
    return data

