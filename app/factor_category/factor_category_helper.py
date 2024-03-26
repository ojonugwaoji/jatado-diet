from .factor_category_schema import FactorCategorySchema


def deserialize_factor_category(factor_category) -> dict:
    return FactorCategorySchema(**factor_category)
