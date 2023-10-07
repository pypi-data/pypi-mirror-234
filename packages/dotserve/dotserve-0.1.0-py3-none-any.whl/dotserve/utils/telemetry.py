"""Anonymous telemetry for Dotserve."""

from __future__ import annotations

import json
import multiprocessing
import platform
from datetime import datetime

import httpx
import psutil

from dotserve import constants
from dotserve.base import Base
from dotserve.config import get_config


def get_os() -> str:
    """Get the operating system.

    Returns:
        The operating system.
    """
    return platform.system()


def get_python_version() -> str:
    """Get the Python version.

    Returns:
        The Python version.
    """
    return platform.python_version()


def get_dotserve_version() -> str:
    """Get the Dotserve version.

    Returns:
        The Dotserve version.
    """
    return constants.Dotserve.VERSION


def get_cpu_count() -> int:
    """Get the number of CPUs.

    Returns:
        The number of CPUs.
    """
    return multiprocessing.cpu_count()


def get_memory() -> int:
    """Get the total memory in MB.

    Returns:
        The total memory in MB.
    """
    return psutil.virtual_memory().total >> 20


class Telemetry(Base):
    """Anonymous telemetry for Dotserve."""

    user_os: str = get_os()
    cpu_count: int = get_cpu_count()
    memory: int = get_memory()
    dotserve_version: str = get_dotserve_version()
    python_version: str = get_python_version()


def send(event: str, telemetry_enabled: bool | None = None) -> bool:
    """Send anonymous telemetry for Dotserve.

    Args:
        event: The event name.
        telemetry_enabled: Whether to send the telemetry (If None, get from config).

    Returns:
        Whether the telemetry was sent successfully.
    """
    # Get the telemetry_enabled from the config if it is not specified.
    if telemetry_enabled is None:
        telemetry_enabled = get_config().telemetry_enabled

    # Return if telemetry is disabled.
    if not telemetry_enabled:
        return False

    try:
        telemetry = Telemetry()
        with open(constants.DOTSERVE_JSON) as f:  # type: ignore
            dotserve_json = json.load(f)
            distinct_id = dotserve_json["project_hash"]
        post_hog = {
            "api_key": "phc_JoMo0fOyi0GQAooY3UyO9k0hebGkMyFJrrCw1Gt5SGb",
            "event": event,
            "properties": {
                "distinct_id": distinct_id,
                "user_os": telemetry.user_os,
                "dotserve_version": telemetry.dotserve_version,
                "python_version": telemetry.python_version,
                "cpu_count": telemetry.cpu_count,
                "memory": telemetry.memory,
            },
            "timestamp": datetime.utcnow().isoformat(),
        }
        httpx.post("https://app.posthog.com/capture/", json=post_hog)
        return True
    except Exception:
        return False
