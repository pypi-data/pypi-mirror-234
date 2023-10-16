from typing import Optional

from sentry_sdk import capture_message

from slingshot import schemas


def describe_component_type(component_type: schemas.ComponentType, app_sub_type: Optional[schemas.AppSubType]) -> str:
    """Describes an "app" in the broader sense (including sessions, runs, deployments, etc.)"""

    if component_type == schemas.ComponentType.RUN:
        return "run"
    elif component_type == schemas.ComponentType.DEPLOYMENT:
        return "deployment"
    elif component_type == schemas.ComponentType.APP:
        if app_sub_type == schemas.AppSubType.SESSION:
            return "session"
        else:
            return "app"
    else:
        capture_message("Asked to format unknown component type {component_type}, defaulting to 'app'")
        return "app"
