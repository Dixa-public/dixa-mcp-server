"""Get API key information and organization details from Dixa"""
import os
import json
from tools.utils import get_api_key, make_request


def mask_api_key(api_key: str) -> str:
    """
    Mask an API key showing only the first 4 and last 4 characters.
    
    Args:
        api_key: The API key to mask
    
    Returns:
        Masked API key string (e.g., "dixa_xxxx...xxxx")
    """
    if len(api_key) <= 8:
        return "*" * len(api_key)
    
    return f"{api_key[:4]}...{api_key[-4:]}"


def get_api_info(log=None, session=None) -> str:
    """
    Get information about the configured Dixa API key and the associated organization.
    
    This tool shows:
    - A masked version of the API key (first 4 and last 4 characters)
    - Organization information from Dixa API
    
    Args:
        log: Optional logger for debugging
        session: Optional session context that may contain auth information
    
    Returns:
        JSON string containing API key info and organization details
    """
    try:
        api_key = get_api_key(session)
        masked_key = mask_api_key(api_key)
        
        if log:
            log.debug("Fetching organization information")
        
        # Try to get organization info from Dixa API
        # Common endpoints: /v1/organization, /v1/organizations, /v1/me
        organization_info = None
        error_message = None
        
        # Try /v1/organization endpoint first
        try:
            url = "https://dev.dixa.io/v1/organization"
            org_data = make_request("GET", url, log=log, session=session)
            organization_info = json.loads(org_data)
            # Handle case where response is wrapped in 'data' key
            if isinstance(organization_info, dict) and "data" in organization_info:
                organization_info = organization_info["data"]
        except Exception as e:
            error_message = str(e)
            # Try alternative endpoint /v1/organizations
            try:
                url = "https://dev.dixa.io/v1/organizations"
                org_data = make_request("GET", url, log=log, session=session)
                organization_info = json.loads(org_data)
                # Handle case where response is wrapped in 'data' key
                if isinstance(organization_info, dict) and "data" in organization_info:
                    organization_info = organization_info["data"]
                error_message = None
            except Exception:
                pass
        
        result = {
            "api_key": {
                "masked": masked_key,
                "length": len(api_key),
                "is_set": True
            },
            "organization": organization_info if organization_info else None,
            "error": error_message if error_message else None
        }
        
        return json.dumps(result, indent=2)
        
    except ValueError as e:
        # API key not set
        return json.dumps({
            "api_key": {
                "masked": "NOT SET",
                "length": 0,
                "is_set": False
            },
            "organization": None,
            "error": str(e)
        }, indent=2)
    except Exception as e:
        return json.dumps({
            "api_key": {
                "masked": "ERROR",
                "length": 0,
                "is_set": False
            },
            "organization": None,
            "error": str(e)
        }, indent=2)

