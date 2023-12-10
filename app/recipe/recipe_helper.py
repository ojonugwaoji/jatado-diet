from .recipe_schema import Recipe


def deserialize_recipe(recipe) -> dict:
    return Recipe(**recipe)
