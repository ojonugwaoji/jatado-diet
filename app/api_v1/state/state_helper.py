from .state_schema import State


def deserialize_state(state) -> dict:
    # return None if state == None else State(**state)
    return State(**state)
