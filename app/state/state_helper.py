from .state_schema import State


def deserialize_state(state) -> dict:
    # return None if state == None else State(**state)
    id = state["_id"]
    #state["_id"] = state.pop("id", None)
    if 'key' in state: del state['key']
    state["id"] = id
    return State(**state)
