/**
 * Utility functions for Dixa API calls
 */

/**
 * Gets the Dixa API key from environment variables with validation
 * @throws Error if the API key is not set or is empty
 */
export function getDixaApiKey(): string {
  if (!process.env.DIXA_API_KEY) {
    throw new Error(
      'DIXA_API_KEY environment variable is not set. Please set it in your FastMCP Cloud dashboard under Environment Variables.'
    );
  }

  const apiKey = process.env.DIXA_API_KEY.trim();
  if (!apiKey) {
    throw new Error(
      'DIXA_API_KEY environment variable is set but is empty. Please check your FastMCP Cloud dashboard settings.'
    );
  }

  return apiKey;
}

/**
 * Creates the Authorization header value with Bearer prefix
 */
export function getAuthHeader(): string {
  return `Bearer ${getDixaApiKey()}`;
}

/**
 * Creates a helpful error message for 401 authentication errors
 */
export function createAuthErrorMessage(errorText: string): string {
  return (
    `Authentication failed (401 Unauthorized). This usually means:\n` +
    `1. The DIXA_API_KEY environment variable is not set correctly in FastMCP Cloud dashboard\n` +
    `2. The API key is invalid or has expired\n` +
    `3. The API key format is incorrect\n\n` +
    `Please verify:\n` +
    `- Go to your FastMCP Cloud dashboard\n` +
    `- Check that DIXA_API_KEY is set under Environment Variables\n` +
    `- Ensure there are no extra spaces or quotes around the key\n` +
    `- Verify the API key is valid in your Dixa account\n\n` +
    `Response: ${errorText}`
  );
}

/**
 * Handles HTTP response errors with special handling for 401 errors
 * This is an async helper that should be used with await
 */
export async function handleResponseError(
  resp: Response,
  defaultMessage: string
): Promise<never> {
  const errorText = await resp.text();
  if (resp.status === 401) {
    throw new Error(createAuthErrorMessage(errorText));
  }
  throw new Error(`${defaultMessage}: ${resp.status} ${resp.statusText}\nResponse: ${errorText}`);
}

