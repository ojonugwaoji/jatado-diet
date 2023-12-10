from .user_schema import User


def deserialize_user(user) -> dict:
    return User(**user)
