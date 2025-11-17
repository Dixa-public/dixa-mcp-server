import { z } from "zod";
import { getDixaApiKey } from "../utils";

/**
 * Mask an API key showing only the first 4 and last 4 characters.
 */
function maskApiKey(apiKey: string): string {
  if (apiKey.length <= 8) {
    return "*".repeat(apiKey.length);
  }
  return `${apiKey.substring(0, 4)}...${apiKey.substring(apiKey.length - 4)}`;
}

export const getApiInfo = {
  name: "getApiInfo",
  description: "Preview the configured DIXA_API_KEY (masked) and get information about the associated organization",
  parameters: z.object({}),
  execute: async (args, { log, session }) => {
    let apiKey: string | null = null;
    let maskedKey = "NOT SET";
    let apiKeyLength = 0;
    let isSet = false;

    try {
      apiKey = getDixaApiKey(session);
      maskedKey = maskApiKey(apiKey);
      apiKeyLength = apiKey.length;
      isSet = true;
    } catch (error) {
      const errorMessage = error instanceof Error ? error.message : String(error);
      return {
        type: "text" as const,
        text: JSON.stringify({
          api_key: {
            masked: "NOT SET",
            length: 0,
            is_set: false,
          },
          organization: null,
          error: errorMessage,
        }, null, 2),
      };
    }

    // Try to get organization info from Dixa API
    let organizationInfo: any = null;
    let errorMessage: string | null = null;

    // Try /v1/organization endpoint first
    try {
      const url = "https://dev.dixa.io/v1/organization";
      log.debug("Request URL:", url);

      const resp = await fetch(url, {
        method: "GET",
        headers: {
          Authorization: `Bearer ${apiKey}`,
          "Content-Type": "application/json",
        },
      });

      if (resp.ok) {
        const data = await resp.json();
        // Handle case where response is wrapped in 'data' key
        organizationInfo = data?.data || data;
      } else {
        const errorText = await resp.text();
        errorMessage = `Failed to fetch organization: ${resp.status} ${resp.statusText}\nResponse: ${errorText}`;
        
        // Try alternative endpoint /v1/organizations
        try {
          const altUrl = "https://dev.dixa.io/v1/organizations";
          log.debug("Trying alternative URL:", altUrl);

          const altResp = await fetch(altUrl, {
            method: "GET",
            headers: {
              Authorization: `Bearer ${apiKey}`,
              "Content-Type": "application/json",
            },
          });

          if (altResp.ok) {
            const altData = await altResp.json();
            organizationInfo = altData?.data || altData;
            errorMessage = null;
          } else {
            const altErrorText = await altResp.text();
            errorMessage = `Failed to fetch organization from both endpoints. Last error: ${altResp.status} ${altResp.statusText}\nResponse: ${altErrorText}`;
          }
        } catch (altError) {
          // Keep the original error message
        }
      }
    } catch (error) {
      errorMessage = error instanceof Error ? error.message : String(error);
    }

    const result = {
      api_key: {
        masked: maskedKey,
        length: apiKeyLength,
        is_set: isSet,
      },
      organization: organizationInfo,
      error: errorMessage,
    };

    return {
      type: "text" as const,
      text: JSON.stringify(result, null, 2),
    };
  },
};

