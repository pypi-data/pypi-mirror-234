# msgraph-py

## Description
Collection of functions for easily using Microsoft Graph API in Python.

## Getting Started
1. Create an app registration in Azure with the necessary permissions:  
[Authentication and authorization steps](https://learn.microsoft.com/en-us/graph/auth-v2-service?tabs=http#authentication-and-authorization-steps)

2. Install dependencies:  
`$ pip install --user -r requirements.txt`

3. Set environment variables:
    * If the package is used in a Django app, create and populate the following variables in the project's `settings.py`:

        ```python
        AAD_TENANT_ID = ""
        AAD_CLIENT_ID = ""
        AAD_CLIENT_SECRET = ""
        ```

    * If the package is used directly from a Python script, copy `settings_sample.json` → `settings.json` and configure the environment variables in the JSON file.
    * This logic can be customized as needed in [`msgraph.config`](/msgraph/config.py)

## Examples
```python
import msgraph


# Fetches a single user
# Username can be objectId or userPrincipalName
user = msgraph.get_user("user@example.com")
display_name = user["displayName"]
print(f"Hello, {display_name}!")


# Fetches multiple users with advanced query parameters
# Sorts by the 10 most recently created users starting with "mailbox-"
filtered_users = msgraph.get_user(
    filter="startsWith(userPrincipalName, 'mailbox-')",
    select=["id", "displayName", "createdDateTime"],
    orderby="createdDateTime desc",
    top=10,
)

for user in filtered_users:
    line = "{};{};{}".format(
        user["id"],
        user["displayName"],
        user["createdDateTime"],
    )
    print(line)


# Sends an email with attachments.
msgraph.send_mail(
    sender="noreply@example.com",
    recipients=[
        "john.doe@example.com",
        "jane.doe@example.com",
    ],
    subject="Mail from Graph API",
    body="<h1>Content of the mail body</h1>",
    is_html=True,
    priority="high",
    attachments=[
        "/path/to/file1.txt",
        "/path/to/file2.docx"
    ],
)
```

## Documentation
- [Authentication and authorization basics](https://learn.microsoft.com/en-us/graph/auth/auth-concepts)
- [Use query parameters to customize responses](https://learn.microsoft.com/en-us/graph/query-parameters)
- [User resource type - Properties](https://learn.microsoft.com/en-us/graph/api/resources/user?view=graph-rest-1.0#properties)
- [Azure AD authentication methods API overview](https://learn.microsoft.com/en-us/graph/api/resources/authenticationmethods-overview)
