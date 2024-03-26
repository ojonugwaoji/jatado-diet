from .factor_score_schema import FactorScoreSchema


def deserialize_factor_score(factor_score) -> dict:
    return FactorScoreSchema(**factor_score)
