from .country_schema import Country


def deserialize_country(country) -> dict:
    return Country(**country)
