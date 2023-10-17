from typing import Optional, Union
from urllib.parse import quote_plus


def create_dsn(
    host: Optional[str] = None,
    port: Optional[Union[str, int]] = None,
    user: Optional[str] = None,
    password: Optional[str] = None,
    database: Optional[str] = None,
    driver: str = "postgresql",
):
    result = f"{driver}://"

    if user:
        result += quote_plus(user)
    if password:
        result += f":{quote_plus(password)}"
    if user or password:
        result += "@"

    if host:
        result += quote_plus(host)
    if port:
        result += f":{quote_plus(str(port))}"

    if database:
        result += f"/{quote_plus(database)}"

    return result
