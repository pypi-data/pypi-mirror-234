import os
import platform
import site
import socket
import sys
import traceback

import click
import requests

from korbit import __version__
from korbit.constant import (
    KORBIT_INSTALLATION_SOURCE_BINARY,
    KORBIT_INSTALLATION_SOURCE_PIP,
    KORBIT_SCAN_TELEMETRY_URL,
)
from korbit.interface import INTERFACE_SOMETHING_WENT_WRONG_MSG
from korbit.login import authenticate_request, get_user_secret_id


def installation_source(command_path: str):
    bin_folder = os.path.dirname(sys.executable)
    binary_path = os.path.join(bin_folder, "korbit")
    site_packages_path = site.getsitepackages()[0]
    if os.path.exists(binary_path) and command_path == binary_path:
        if site_packages_path.startswith(os.path.commonprefix([bin_folder, site_packages_path])):
            return KORBIT_INSTALLATION_SOURCE_PIP
    return KORBIT_INSTALLATION_SOURCE_BINARY


def get_user_agent(command: list[str]):
    user_agent = {
        "os": platform.system(),
        "os_version": platform.release(),
        "architecture": platform.machine(),
        "python_version": sys.version,
        "hostname": socket.gethostname(),
        "cli_version": __version__,
        "command": " ".join(command) if command else "",
        "user_id": get_user_secret_id(),
    }
    if command:
        user_agent["installation_source"] = installation_source(command[0])
    else:
        user_agent["installation_source"] = "unknown"
    return user_agent


def send_telemetry(command: list[str], message: str, error: bool = False):
    log = {
        "version": __version__,
        "user_agent": {},
        "user_secret_id": get_user_secret_id(),
        "type": "ERROR" if error else "INFO",
        "message": message,
    }
    try:
        user_agent = get_user_agent(command)
        log["user_agent"] = user_agent
    except Exception:
        # if user agent isn't computable concat the traceback to the current message.
        log["message"] = f"{message}\n\nSomething wrong happened while computing user agent: {traceback.format_exc()}"

    try:
        authenticate_request(requests.post, KORBIT_SCAN_TELEMETRY_URL, json=log)
    except requests.exceptions.RequestException:
        # We don't want to raise the exception again because it will infinite loop
        click.echo(INTERFACE_SOMETHING_WENT_WRONG_MSG)
