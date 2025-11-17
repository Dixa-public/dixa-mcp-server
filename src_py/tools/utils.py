"""
Utility functions for Dixa API calls
"""
import os
import json
import requests
from typing import Dict, Any, Optional
from contextvars import ContextVar

# Context variable to store the current session/auth
# This allows tools to access the session even if not passed as parameter
_current_session: ContextVar[Optional[Dict[str, Any]]] = ContextVar('_current_session', default=None)


def set_session(session: Optional[Dict[str, Any]]) -> None:
    """Set the current session context (called by FastMCP if session is available)"""
    _current_session.set(session)


def get_current_session() -> Optional[Dict[str, Any]]:
    """Get the current session from context"""
    return _current_session.get()


def get_api_key(session: Optional[Dict[str, Any]] = None) -> str:
    """
    Get the Dixa API key from session context or environment variable.
    Priority: session auth > environment variable
    
    Args:
        session: Optional session context that may contain auth information
                 (for FastMCP Cloud config overrides via 'auth' field)
                 If not provided, will try to get from context variable
    
    Returns:
        The API key string
    """
    # If session not provided, try to get from context variable
    if session is None:
        session = get_current_session()
    
    # First, try to get API key from session context (for FastMCP Cloud config overrides)
    # The auth object from MCP config is passed as the session
    # FastMCP Cloud might pass it as: { "DIXA_API_KEY": "..." } or { "apiKey": "..." }
    if session:
        # Check common auth field names that might be used in MCP config
        # FastMCP Cloud passes auth object like: { "apiKey": "..." }
        session_api_key = None
        
        # Try different field names in order of likelihood
        # Prioritize DIXA_API_KEY since that's what users might use in config
        for field_name in ["DIXA_API_KEY", "apiKey", "token", "auth", "dixaApiKey"]:
            value = session.get(field_name)
            if value and isinstance(value, str):
                session_api_key = value
                break
        
        if session_api_key:
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
                 If not provided, will try to get from context variable
    
    Returns:
        Formatted JSON string
    """
    # If session not provided, try to get from context variable
    if session is None:
        session = get_current_session()
    
    api_key = get_api_key(session)
    
    # Log that API key is present (without exposing the value)
    if log:
        # Log session info for debugging (without exposing sensitive data)
        session_source = "session" if session else "environment"
        log.debug(f"API key source: {session_source}, length: {len(api_key)} characters")
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

