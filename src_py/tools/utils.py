"""
Utility functions for Dixa API calls
"""
import os
import json
import requests
from typing import Dict, Any, Optional


def get_api_key(session: Optional[Dict[str, Any]] = None) -> str:
    """
    Get the Dixa API key from session context or environment variable.
    Priority: session auth > environment variable
    
    Args:
        session: Optional session context that may contain auth information
                 (for FastMCP Cloud config overrides via 'auth' field)
    
    Returns:
        The API key string
    """
    # First, try to get API key from session context (for FastMCP Cloud config overrides)
    if session:
        # Check common auth field names that might be used in MCP config
        session_api_key = (
            session.get("apiKey") or
            session.get("token") or
            session.get("auth") or
            session.get("DIXA_API_KEY") or
            session.get("dixaApiKey")
        )
        
        if session_api_key and isinstance(session_api_key, str):
            trimmed = session_api_key.strip()
            if trimmed:
                return trimmed
    
    # Fall back to environment variable
    api_key = os.getenv("DIXA_API_KEY")
    if not api_key:
        # Check if the variable exists but is empty
        if "DIXA_API_KEY" in os.environ:
            raise ValueError(
                "DIXA_API_KEY environment variable is set but is empty. "
                "Please check your FastMCP Cloud dashboard settings."
            )
        raise ValueError(
            "DIXA_API_KEY environment variable is not set. "
            "Please set it in your FastMCP Cloud dashboard under Environment Variables "
            "or provide it via the 'auth' field in MCP server configuration."
        )
    # Trim whitespace in case there are accidental spaces
    api_key = api_key.strip()
    if not api_key:
        raise ValueError(
            "DIXA_API_KEY environment variable contains only whitespace. "
            "Please check your FastMCP Cloud dashboard settings."
        )
    return api_key


def make_request(
    method: str,
    url: str,
    params: Optional[Dict[str, Any]] = None,
    json_data: Optional[Dict[str, Any]] = None,
    log=None,
    session: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """
    Make an HTTP request to the Dixa API.
    
    Args:
        method: HTTP method (GET, POST, PUT, DELETE)
        url: Full URL to request
        params: Query parameters (for GET requests)
        json_data: JSON body (for POST/PUT requests)
        log: Optional logger for debugging
        session: Optional session context that may contain auth information
    
    Returns:
        Formatted JSON string
    """
    api_key = get_api_key(session)
    
    # Log that API key is present (without exposing the value)
    if log:
        log.debug(f"API key is set (length: {len(api_key)} characters)")
        log.debug(f"Request {method} {url}")
        if json_data:
            log.debug(f"Request body: {json.dumps(json_data, indent=2)}")
    
    # Dixa API expects the Authorization header with Bearer prefix
    # Format: "Bearer <api_key>"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    
    try:
        response = requests.request(
            method=method,
            url=url,
            params=params,
            json=json_data,
            headers=headers,
            timeout=30,
        )
        
        response_text = response.text
        
        if not response.ok:
            # Provide more helpful error messages for 401 errors
            if response.status_code == 401:
                error_msg = (
                    f"Authentication failed (401 Unauthorized). "
                    f"This usually means:\n"
                    f"1. The DIXA_API_KEY environment variable is not set correctly in FastMCP Cloud dashboard\n"
                    f"2. The API key is invalid or has expired\n"
                    f"3. The API key format is incorrect\n\n"
                    f"Please verify:\n"
                    f"- Go to your FastMCP Cloud dashboard\n"
                    f"- Check that DIXA_API_KEY is set under Environment Variables\n"
                    f"- Ensure there are no extra spaces or quotes around the key\n"
                    f"- Verify the API key is valid in your Dixa account\n\n"
                    f"Response: {response_text}"
                )
            else:
                error_msg = (
                    f"Failed to fetch data: {response.status_code} {response.reason}\n"
                    f"Response: {response_text}"
                )
            raise Exception(error_msg)
        
        # Handle 204 No Content responses
        if response.status_code == 204:
            return json.dumps({"success": True, "message": "Operation completed successfully"}, indent=2)
        
        # Parse JSON response
        try:
            data = response.json()
            # Return as formatted JSON string for MCP
            return json.dumps(data, indent=2)
        except json.JSONDecodeError:
            raise Exception(f"Invalid JSON response from server: {response_text}")
            
    except requests.exceptions.RequestException as e:
        raise Exception(f"Request failed: {str(e)}")

