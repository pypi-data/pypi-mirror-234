import base64
import json
import os
from pathlib import Path
from typing import Callable, Optional

import requests

from korbit.interface import (
    INTERFACE_AUTH_MISSING_CREDENTIALS_MSG,
    INTERFACE_AUTH_UNAUTHORIZED_CREDENTIALS_MSG,
    INTERFACE_UPDATE_REQUIRED_MSG,
)

KORBIT_CREDENTIAL_FILE = os.path.expanduser("~/.korbit/credentials")


class KorbitAuthError(Exception):
    pass


class CLIVersionDeprecated(Exception):
    pass


def store_credentials(secret_id, secret_key):
    """
    Store user credentials for future usage of scan command.
    """
    os.makedirs(Path(KORBIT_CREDENTIAL_FILE).parent, exist_ok=True)
    with open(KORBIT_CREDENTIAL_FILE, "w+") as credential_file:
        json.dump({"secret_id": secret_id, "secret_key": secret_key}, credential_file)


def get_credential() -> dict:
    credentials = {}
    if os.path.exists(KORBIT_CREDENTIAL_FILE):
        with open(KORBIT_CREDENTIAL_FILE, "r+") as credential_file:
            credentials = json.loads(credential_file.read())
    return credentials


def compute_user_token():
    credentials = get_credential()
    secret_id = os.getenv("KORBIT_SECRET_ID", credentials.get("secret_id"))
    secret_key = os.getenv("KORBIT_SECRET_KEY", credentials.get("secret_key"))

    if not secret_id or not secret_key:
        raise KorbitAuthError(INTERFACE_AUTH_MISSING_CREDENTIALS_MSG)
    return base64.b64encode(f"{secret_id}:{secret_key}".encode()).decode()


def get_user_secret_id() -> Optional[str]:
    credentials = get_credential()
    return os.getenv("KORBIT_SECRET_ID", credentials.get("secret_id"))


def authenticate_request(method: Callable[[str], requests.Response], url: str, **kwargs) -> requests.Response:
    headers = kwargs.pop("headers", {})
    if not headers.get("Authorization"):
        headers["Authorization"] = f"Basic {compute_user_token()}"

    kwargs["headers"] = headers
    response = method(url, **kwargs)
    if response.status_code in [401, 403]:
        raise KorbitAuthError(INTERFACE_AUTH_UNAUTHORIZED_CREDENTIALS_MSG)
    if response.status_code == 410:
        raise CLIVersionDeprecated(response.json().get("message", INTERFACE_UPDATE_REQUIRED_MSG))
    response.raise_for_status()
    return response
