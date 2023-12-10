from .ethnicity_schema import EthnicitySchema


def deserialize_ethnicity(ethnicity) -> dict:
    return EthnicitySchema(**ethnicity)
