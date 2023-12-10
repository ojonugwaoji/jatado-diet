from .language_schema import Language


def deserialize_language(language) -> dict:
    return Language(**language)
