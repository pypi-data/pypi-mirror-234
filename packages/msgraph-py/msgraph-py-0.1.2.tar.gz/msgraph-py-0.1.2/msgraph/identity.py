from typing import Union

import requests

from .auth import get_token


def get_user(
    user_id: str = None,
    select: Union[list, str] = None,
    filter: str = None,
    search: str = None,
    orderby: Union[list, str] = None,
    top: int = None,
    all: bool = False,
) -> Union[list[dict], dict]:
    """
    Returns one or more users from the Microsoft Graph API.
    The parameters select, filter, search, and orderby use OData queries:
    https://learn.microsoft.com/en-us/graph/query-parameters

    Supports paging and limits the result to the first 100 objects by default.
    This can be specified by setting top=[1..999], or all=True to iterate
    through all pages and return all objects.

    Requires admin consent for "User.Read.All" app permissions in the client.

    API documentation:
    https://learn.microsoft.com/en-us/graph/api/resources/user
    https://learn.microsoft.com/en-us/graph/api/user-list

    """

    MAX_PAGE_SIZE = 999

    def ensure_list(value):
        return [value] if isinstance(value, str) else value

    if user_id and (filter or search):
        raise ValueError("Parameters user_id and filter|search are mutually exclusive.")

    headers = {
        "Authorization": f"Bearer {get_token()}",
        "ConsistencyLevel": "eventual" if filter or search or orderby else None,
    }

    params = {
        "$select": ",".join(ensure_list(select)) if select else None,
        "$filter": filter,
        "$search": f'"{search}"' if search else None,
        "$orderby": ",".join(ensure_list(orderby)) if orderby else None,
        "$top": top if top is not None else (MAX_PAGE_SIZE if all else None),
        "$count": "true" if filter or search or orderby else None,
    }

    data = []
    url = "https://graph.microsoft.com/v1.0/users"

    if user_id:
        url += f"/{user_id}"

    while True:
        response = requests.get(url, headers=headers, params=params)

        if response.status_code != 200:
            error_message = response.json().get("error", {}).get("message")
            raise ConnectionError(
                f"Request failed ({response.status_code} {response.reason}):\n"
                f"{error_message}"
            )

        data.extend(response.json().get("value", [response.json()]))
        next_link = response.json().get("@odata.nextLink")

        if next_link and (all and top is None):
            params["$skiptoken"] = next_link.split("$skiptoken=")[1]
        else:
            break

    return data[0] if user_id else data


def revoke_refresh_tokens(user_id: str) -> bool:
    """
    Revokes all refresh tokens for a given user.

    Requires admin consent for "User.ReadWrite.All" app permissions.

    API documentation:
    https://learn.microsoft.com/en-us/graph/api/user-revokesigninsessions
    """
    response = requests.post(
        url=f"https://graph.microsoft.com/v1.0/users/{user_id}/revokeSignInSessions",
        headers={"Authorization": f"Bearer {get_token()}"},
    )

    if response.status_code != 200:
        error_message = response.json().get("error", {}).get("message")
        raise ConnectionError(
            f"Request failed ({response.status_code} {response.reason}):\n"
            f"{error_message}"
        )

    return response.json()["value"]


def list_auth_methods(user_id: str) -> list[dict]:
    """
    Returns a list of all authentication methods for a given user.

    Requires admin consent for "UserAuthenticationMethod.Read.All" app permissions.

    API documentation:
    https://learn.microsoft.com/en-us/graph/api/authentication-list-methods

    """

    response = requests.get(
        url=f"https://graph.microsoft.com/v1.0/users/{user_id}/authentication/methods",
        headers={"Authorization": f"Bearer {get_token()}"},
    )

    if response.status_code != 200:
        error_message = response.json().get("error", {}).get("message")
        raise ConnectionError(
            f"Request failed ({response.status_code} {response.reason}):\n"
            f"{error_message}"
        )

    return response.json()["value"]


def delete_auth_method(user_id: str, auth_method: dict) -> bool:
    """
    Deletes an authentication method for a user and returns True or False.
    Expects a dictionary object in the auth_method parameter from list_auth_methods()
    to find the method's id and @odata.type since each authentication method resides
    in its own endpoint and must be mapped based on its type.

    Requires admin consent for "UserAuthenticationMethod.ReadWrite.All" app permissions.

    API documentation:
    https://learn.microsoft.com/en-us/graph/api/resources/authenticationmethods-overview

    """

    method_id = auth_method["id"]
    odata_type = auth_method["@odata.type"]

    if odata_type == "#microsoft.graph.microsoftAuthenticatorAuthenticationMethod":
        endpoint = "microsoftAuthenticatorMethods"
    elif odata_type == "#microsoft.graph.phoneAuthenticationMethod":
        endpoint = "phoneMethods"
    elif odata_type == "#microsoft.graph.softwareOathAuthenticationMethod":
        endpoint = "softwareOathMethods"
    elif odata_type == "#microsoft.graph.fido2AuthenticationMethod":
        endpoint = "fido2Methods"
    elif odata_type == "#microsoft.graph.windowsHelloForBusinessAuthenticationMethod":
        endpoint = "windowsHelloForBusinessMethods"
    elif odata_type == "#microsoft.graph.emailAuthenticationMethod":
        endpoint = "emailMethods"
    else:
        return False

    response = requests.delete(
        url=f"https://graph.microsoft.com/v1.0/users/{user_id}/authentication/{endpoint}/{method_id}",
        headers={"Authorization": f"Bearer {get_token()}"},
    )

    if response.status_code != 204:
        error_message = response.json().get("error", {}).get("message")
        raise ConnectionError(
            f"Request failed ({response.status_code} {response.reason}):\n"
            f"{error_message}"
        )

    return True


def reset_strong_auth(user_id: str) -> bool:
    """
    Resets 2FA by deleting the user's registered authentication methods.
    The API has no way to check the default method, which must be deleted last.
    A work-around is to temporarily store the method from the failed request
    and try again after the loop.

    Requires admin consent for "UserAuthenticationMethod.ReadWrite.All" and
    "User.ReadWrite.All" app permissions.

    """

    default_method = None

    revoke_refresh_tokens(user_id)

    for method in list_auth_methods(user_id):
        try:
            delete_auth_method(user_id, method)
        except ConnectionError:
            if not default_method:
                default_method = method
                continue
            else:
                raise
    if default_method:
        delete_auth_method(user_id, default_method)

    return True


def get_user_risk(
    user_id: str = None,
    select: Union[list, str] = None,
    filter: str = None,
    search: str = None,
    orderby: Union[list, str] = None,
    top: int = None,
    all: bool = False,
) -> Union[list[dict], dict]:
    """
    Returns the user risk status for one or more users from the Microsoft Graph API.
    The parameters select, filter, search, and orderby use OData queries:
    https://learn.microsoft.com/en-us/graph/query-parameters

    Supports paging and limits the result to the first 20 objects by default.
    This can be specified by setting top=[1..500], or all=True to iterate
    through all pages and return all objects.

    Requires admin consent for "IdentityRiskyUser.Read.All" app permissions in the
    client.

    API documentation:
    https://learn.microsoft.com/en-us/graph/api/resources/riskyuser
    https://learn.microsoft.com/en-us/graph/api/riskyuser-list

    """

    MAX_PAGE_SIZE = 500

    def ensure_list(value):
        return [value] if isinstance(value, str) else value

    if user_id and (filter or search):
        raise ValueError("Parameters user_id and filter|search are mutually exclusive.")

    headers = {
        "Authorization": f"Bearer {get_token()}",
        "ConsistencyLevel": "eventual" if filter or search or orderby else None,
    }

    params = {
        "$select": ",".join(ensure_list(select)) if select else None,
        "$filter": filter,
        "$search": f'"{search}"' if search else None,
        "$orderby": ",".join(ensure_list(orderby)) if orderby else None,
        "$top": top if top is not None else (MAX_PAGE_SIZE if all else None),
        "$count": "true" if filter or search or orderby else None,
    }

    data = []
    url = "https://graph.microsoft.com/v1.0/identityProtection/riskyUsers"

    if user_id:
        url += f"/{user_id}"

    while True:
        response = requests.get(url, headers=headers, params=params)

        if response.status_code != 200:
            error_message = response.json().get("error", {}).get("message")
            raise ConnectionError(
                f"Request failed ({response.status_code} {response.reason}):\n"
                f"{error_message}"
            )

        data.extend(response.json().get("value", [response.json()]))
        next_link = response.json().get("@odata.nextLink")

        if next_link and (all and top is None):
            params["$skiptoken"] = next_link.split("$skiptoken=")[1]
        else:
            break

    return data[0] if user_id else data
