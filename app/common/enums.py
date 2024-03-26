from enum import Enum


class Tag(str, Enum):
    MISC = 'Miscellaneous'
    AUTHENTICATION = 'Authentication'
    USER = 'Users'
    COUNTRY = 'Countries'
    STATE = 'States'
    LGA = 'LGAs'
    RECIPE_UNIT_SCHEME = 'Recipe Unit Scheme'
    RECIPE_QUANTITY = 'Recipe Quantity'
    ACTION = 'Actions'
    ETHNICITY = 'Ethnicity'
    LANGUAGE = 'Language'
    NUTRIENT = 'Nutrients'
    FOOD_ITEM = 'Food Item'
    DISH = "Dishes"
    FACTOR_CATEGORY = "Factor Category"
    FACTOR = "Factor"
    FACTOR_SCORE = "Factor Score"


class Environment(str, Enum):
    TEST = 'test'
    DEVELOPMENT = 'development'
    PRODUCTION = 'production'
