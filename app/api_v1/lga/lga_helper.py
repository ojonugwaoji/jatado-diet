from .lga_schema import Lga


def deserialize_lga(lga) -> dict:
    return Lga(**lga)
