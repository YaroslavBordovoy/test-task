def id_validator(id: int) -> None:
    if id < 0:
        raise ValueError("The id cannot be less than 0.")


def price_validator(price: float) -> None:
    if price <= 0:
        raise ValueError("The price cannot be less than or equal to 0.")


def string_validator(string: str) -> None:
    if not isinstance(string, str):
        raise TypeError("Data is not a string.")