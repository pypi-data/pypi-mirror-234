from time import time

import requests

from .config import get_config

CLOCK_SKEW_SECONDS = 5 * 60
token_cache = {}


def get_token() -> str:
    """
    Returns an access token for the client in Azure AD.
    Uses the same token from token_cache in repeated API-calls.

    Documentation:
    https://learn.microsoft.com/en-us/graph/auth/auth-concepts

    """

    global token_cache
    if token_cache:
        if token_cache["exp"] >= time() + CLOCK_SKEW_SECONDS:
            return token_cache["jwt"]

    (tenant_id, client_id, client_secret) = get_config()

    response = requests.post(
        url=f"https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/token",
        data={
            "grant_type": "client_credentials",
            "scope": "https://graph.microsoft.com/.default",
            "client_id": client_id,
            "client_secret": client_secret,
        },
    )
    if response.status_code != 200:
        error_message = response.json().get("error_description")
        raise ConnectionError(
            f"Request failed ({response.status_code} {response.reason}):\n"
            f"{error_message}"
        )
    response = response.json()
    token_cache["jwt"] = response["access_token"]
    token_cache["exp"] = time() + response["expires_in"]

    return response["access_token"]


def clear_cache():
    global token_cache
    if token_cache:
        del token_cache
