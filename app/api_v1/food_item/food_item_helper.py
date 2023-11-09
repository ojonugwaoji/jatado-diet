from .food_item_schema import FoodItem, CreateFoodItemDto


def deserialize_food_item(food_item) -> dict:
    return FoodItem(**food_item)


def deserialize_create_food_item_dto(food_item) -> dict:
    return CreateFoodItemDto(**food_item)
