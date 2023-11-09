from .recipe_unit_scheme_schema import RecipeUnitScheme


def deserialize_recipe_unit_scheme(recipe_unit_scheme) -> dict:
    return RecipeUnitScheme(**recipe_unit_scheme)
