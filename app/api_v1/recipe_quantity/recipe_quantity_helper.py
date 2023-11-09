from .recipe_quantity_schema import RecipeQuantity


def deserialize_recipe_quantity(recipe_quantity) -> dict:
    return RecipeQuantity(**recipe_quantity)
