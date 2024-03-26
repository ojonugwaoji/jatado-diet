from .dish_schema import Dish


def deserialize_dish(dish) -> dict:
    return Dish(**dish)
