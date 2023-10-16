import traceback

import requests

from korbit import __version__
from korbit.constant import KORBIT_INSTALLATION_SOURCE_PIP, KORBIT_SCAN_VERSION_URL
from korbit.interface import INTERFACE_UPDATE_REQUIRED_MSG, print_markdown_message
from korbit.login import CLIVersionDeprecated, authenticate_request
from korbit.telemetry import get_user_agent, send_telemetry


def should_update(command: list[str]):
    try:
        user_agent = get_user_agent(command)
    except Exception:
        send_telemetry([""], f"User agent not computable: {traceback.format_exc()}", error=True)
        user_agent = {}
    try:
        query_params = {
            "version": __version__,
            "architecture": user_agent.get("architecture", "x86_64"),
            "os": user_agent.get("os", "Darwin"),
        }
        headers = {"User-Agent": str(user_agent)}
        authenticate_request(
            requests.get, f"{KORBIT_SCAN_VERSION_URL}?version={__version__}", params=query_params, headers=headers
        )
        return False
    except CLIVersionDeprecated as e:
        if user_agent.get("installation_source") == KORBIT_INSTALLATION_SOURCE_PIP:
            print_markdown_message(INTERFACE_UPDATE_REQUIRED_MSG)
        else:
            print_markdown_message(str(e))
        return True
