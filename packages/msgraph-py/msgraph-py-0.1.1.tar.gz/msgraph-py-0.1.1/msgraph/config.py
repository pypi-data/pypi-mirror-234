import json
import os.path

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SETTINGS_PATH = os.path.join(ROOT_DIR, "settings.json")
PROJECT_NAME = "config"


def get_config(path: str = None) -> tuple[str]:
    """
    Returns a tuple with variables for connecting to the Azure AD client.
    Attempts to read from settings.py if it's run inside a Django project,
    and alternatively falls back to importing a JSON file from SETTINGS_PATH.

    The path to the settings file can be overridden by setting the path parameter.

    """

    if not path:
        try:
            from django.conf import settings

            # Hvis settings.py ikke er intialisert
            if not settings.configured:
                os.environ.setdefault(
                    "DJANGO_SETTINGS_MODULE", f"{PROJECT_NAME}.settings"
                )
            return (
                settings.AAD_TENANT_ID,
                settings.AAD_CLIENT_ID,
                settings.AAD_CLIENT_SECRET,
            )
        # Django er ikke installert
        except ImportError:
            path = SETTINGS_PATH

    with open(path) as file:
        settings = json.load(file)
    return (
        settings["aad_tenant_id"],
        settings["aad_client_id"],
        settings["aad_client_secret"],
    )
