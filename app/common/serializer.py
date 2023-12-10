from fastapi.encoders import jsonable_encoder


def serialize(model) -> dict:
    return jsonable_encoder(model)
