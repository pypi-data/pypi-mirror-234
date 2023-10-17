import base64
import mimetypes
import os.path
from typing import Union

import requests

from .auth import get_token

VALID_PRIORITY = ["low", "normal", "high"]


def send_mail(
    sender: str,
    recipients: Union[list, str],
    subject: str,
    body: str,
    is_html: bool = False,
    priority: str = "normal",
    recipients_cc: Union[list, str] = [],
    recipients_bcc: Union[list, str] = [],
    attachments: Union[list, str] = [],
    save_sent_items: bool = False,
) -> bool:
    """
    Sends an email on behalf of a user via the Microsoft Graph API.
    Does not save sent items unless save_sent_items=True is set.

    Attachments are added as file paths in the attachments parameter.
    The total size with attachments must not exceed 3MB:
    https://learn.microsoft.com/en-us/graph/api/resources/fileattachment

    Requires admin consent for "Mail.Send" app permissions in the AAD client.

    Note that this permission grants the app access to send emails as any
    user in the organization. This can be restricted with an application access policy:
    https://learn.microsoft.com/en-us/graph/auth-limit-mailbox-access

    API documentation:
    https://learn.microsoft.com/en-us/graph/api/user-sendmail

    """

    def ensure_list(value):
        return [value] if isinstance(value, str) else value

    if priority.lower() not in VALID_PRIORITY:
        raise ValueError(
            f"Parameter priority='{priority}' is not a valid value {VALID_PRIORITY}"
        )

    if is_html:
        content_type = "HTML"
    else:
        content_type = "Text"

    recipients = ensure_list(recipients)
    recipients_cc = ensure_list(recipients_cc)
    recipients_bcc = ensure_list(recipients_bcc)
    attachments = ensure_list(attachments)

    attachments_formatted = []

    for path in attachments:
        if not os.path.isfile(path):
            raise FileNotFoundError(f"File '{path}' was not found.")

        with open(path, mode="rb") as binary:
            encoded_attachment = base64.b64encode(binary.read()).decode("utf-8")

        attachments_formatted.append(
            {
                "@odata.type": "#microsoft.graph.fileAttachment",
                "name": os.path.basename(path),
                "contentType": mimetypes.guess_type(path)[0],
                "contentBytes": encoded_attachment,
            }
        )

    payload = {
        "message": {
            "subject": subject,
            "body": {"contentType": content_type, "content": body},
            "toRecipients": [
                {"emailAddress": {"address": address}} for address in recipients
            ],
            "ccRecipients": [
                {"emailAddress": {"address": address}} for address in recipients_cc
            ],
            "bccRecipients": [
                {"emailAddress": {"address": address}} for address in recipients_bcc
            ],
            "importance": priority,
            "attachments": attachments_formatted,
        },
        "saveToSentItems": save_sent_items,
    }

    response = requests.post(
        url=f"https://graph.microsoft.com/v1.0/users/{sender}/sendMail",
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {get_token()}",
        },
        json=payload,
    )

    if response.status_code != 202:
        error_message = response.json().get("error", {}).get("message")
        raise ConnectionError(
            f"Request failed ({response.status_code} {response.reason}):\n"
            f"{error_message}"
        )

    return True
