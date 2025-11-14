"""Add a tag to a specific conversation in Dixa"""
from tools.utils import make_request


def tag_conversation(conversation_id: str, tag_id: str, log=None) -> str:
    """
    Add a tag to a specific conversation in Dixa.
    
    Args:
        conversation_id: The ID of the conversation to tag
        tag_id: The ID of the tag to add to the conversation
        log: Optional logger for debugging
    
    Returns:
        JSON string indicating success or error
    """
    url = f"https://dev.dixa.io/v1/conversations/{conversation_id}/tags/{tag_id}"
    data = make_request("PUT", url, log=log)
    return data

