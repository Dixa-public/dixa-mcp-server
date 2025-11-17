# FastMCP Cloud Configuration Guide

This guide explains how to configure the Dixa MCP Server to work with FastMCP Cloud and support per-user API keys.

## Overview

The Dixa MCP Server supports two ways to provide the API key:

1. **Environment Variable** (shared for all users): Set `DIXA_API_KEY` in FastMCP Cloud dashboard
2. **Auth Field** (per-user): Pass API key via the `auth` field in MCP client configuration

The server prioritizes the `auth` field over environment variables, allowing different users to use different Dixa API keys.

## Configuration Options

### Option 1: Using the `auth` Field (Recommended for Multi-User)

Configure your MCP client (e.g., Claude Desktop) to pass the API key via the `auth` field:

```json
{
  "mcpServers": {
    "dixa-mcp-server": {
      "command": "npx",
      "args": [
        "-y",
        "mcp-remote",
        "https://your-deployment.fastmcp.app/mcp"
      ],
      "auth": {
        "apiKey": "your_dixa_api_key_here"
      }
    }
  }
}
```

The `auth` object is passed to the server as the session context, and the server extracts the `apiKey` field automatically.

### Option 2: Using Environment Variables (Shared)

Set the `DIXA_API_KEY` environment variable in your FastMCP Cloud dashboard:

1. Go to your FastMCP Cloud project dashboard
2. Navigate to Environment Variables
3. Add `DIXA_API_KEY` with your Dixa API key value
4. Deploy/restart your server

This approach uses the same API key for all users.

### Option 3: Using `env` Field in MCP Config

You can also set environment variables per-client:

```json
{
  "mcpServers": {
    "dixa-mcp-server": {
      "command": "npx",
      "args": [
        "-y",
        "mcp-remote",
        "https://your-deployment.fastmcp.app/mcp"
      ],
      "env": {
        "DIXA_API_KEY": "your_dixa_api_key_here"
      }
    }
  }
}
```

## How It Works

1. **Priority Order**: The server checks for API key in this order:
   - Session context (from `auth` field) - checks for: `apiKey`, `token`, `auth`, `DIXA_API_KEY`, `dixaApiKey`
   - Environment variable `DIXA_API_KEY`

2. **Session Context**: When you use the `auth` field in MCP config, FastMCP Cloud passes that object to the server as the session. The server extracts the API key from common field names.

3. **Fallback**: If no API key is found in the session, it falls back to the environment variable.

## Testing Your Configuration

Use the `getApiInfo` tool to verify your API key configuration:

```json
{
  "tool": "getApiInfo",
  "arguments": {}
}
```

This will show:
- A masked version of the API key being used
- Which source it came from (session or environment)
- Organization information from Dixa API

## Troubleshooting

### 401 Unauthorized Error

If you get a 401 error:

1. **Check API Key Format**: The server automatically adds "Bearer " prefix. Make sure your API key doesn't already include it.
2. **Verify Auth Field**: If using `auth` field, ensure it's an object with `apiKey` field:
   ```json
   "auth": {
     "apiKey": "your_key_here"
   }
   ```
3. **Check Environment Variable**: If using env vars, verify `DIXA_API_KEY` is set correctly in FastMCP Cloud dashboard.
4. **Test with getApiInfo**: Use the `getApiInfo` tool to see which API key is being used.

### API Key Not Found

If you get an error that the API key is not set:

1. Ensure either the `auth` field or `DIXA_API_KEY` environment variable is set
2. Check for typos in field names (should be `apiKey` in the auth object)
3. Verify the API key value is not empty or just whitespace

## Example Configurations

### Claude Desktop Configuration

```json
{
  "mcpServers": {
    "dixa": {
      "command": "npx",
      "args": [
        "-y",
        "mcp-remote",
        "https://dixa-mcp.fastmcp.app/mcp"
      ],
      "auth": {
        "apiKey": "dixa_abc123xyz789..."
      }
    }
  }
}
```

### Using Different Keys for Different Users

Each user can have their own configuration with their own API key:

**User 1's config:**
```json
{
  "mcpServers": {
    "dixa": {
      "command": "npx",
      "args": ["-y", "mcp-remote", "https://dixa-mcp.fastmcp.app/mcp"],
      "auth": {
        "apiKey": "user1_dixa_api_key"
      }
    }
  }
}
```

**User 2's config:**
```json
{
  "mcpServers": {
    "dixa": {
      "command": "npx",
      "args": ["-y", "mcp-remote", "https://dixa-mcp.fastmcp.app/mcp"],
      "auth": {
        "apiKey": "user2_dixa_api_key"
      }
    }
  }
}
```

This allows each user to connect to their own Dixa organization.

