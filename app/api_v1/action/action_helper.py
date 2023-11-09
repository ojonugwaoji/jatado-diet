from .action_schema import Action


def deserialize_action(action) -> dict:
    return Action(**action)
