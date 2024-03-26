from .factor_schema import FactorSchema


def deserialize_factor(factor) -> dict:
    return FactorSchema(**factor)
