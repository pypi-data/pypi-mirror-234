import random
import re
from typing import Callable
from typing import Optional

from h2o_engine_manager.gen.dai_engine_service import ApiException


def generate_engine_id(display_name: str, workspace_id: str, engine_type: str, engine_getter: Callable[[str, str], Optional[ApiException]]) -> str:
    """
    Function generates unused new engine id based on display name.

    Args:
        display_name (str): Display name of an engine.
        workspace_id (str): Workspace id.
        engine_type (str): Engine type like `dai` or `h2o` that will be used to form an engine id if display name is not provided.
        engine_getter (Callable[[str, str], Optional[ApiException]]): Function that returns ApiException in case engine
        identified by engine_id and workspace_id already exists.
    Returns:
        str: An unused engine id.
    """
    if display_name != "":
        display_name = sanitize_display_name(display_name)

    if display_name == "":
        display_name = f"new-{engine_type}-engine"

    for n in range(50):
        if n == 0:
            engine_id = f"{display_name}"
        else:
            engine_id = f"{display_name}-{random.randint(1000,9999)}"
        try:
            engine_getter(engine_id=engine_id, workspace_id=workspace_id)
        except ApiException as e:
            if e.status == 404:
                return engine_id
            else:
                continue

    raise Exception("Unable to generate random unused engine_id, please provide one manually.")

def sanitize_display_name(display_name: str) -> str:
    """
    Function sanitizes display name of an engine to be a valid engine id string.

    Args:
        display_name (str): Display name of an engine.
    Returns:
        str: Sanitized display name of an engine.
    """
    # lowercase
    sanitized = display_name.lower()
    # replace all spaces and _ characters with -
    sanitized = sanitized.replace(" ", "-")
    sanitized = sanitized.replace("_", "-")
    # strip of -
    sanitized = sanitized.strip("-")
    # remove non-alphabetic leading characters
    for n in sanitized:
        if n.isalpha():
            break
        sanitized = sanitized[1:]
    # remove non-alphanumeric characters except of -
    sanitized = re.sub(r"[^a-zA-Z0-9-]", "", sanitized)
    # trim if too long, max 63 characters minus 4 for random suffix = 59
    return sanitized[:58]