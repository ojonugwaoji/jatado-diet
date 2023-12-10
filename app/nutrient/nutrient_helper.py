from .nutrient_schema import Nutrient


def deserialize_nutrient(nutrient) -> dict:
    # return None if nutrient == None else Nutrient(**nutrient)
    return Nutrient(**nutrient)
