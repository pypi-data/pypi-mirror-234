from typing import Callable, TypeVar


T = TypeVar("T")


def get_row_parser(row_class: T) -> Callable[[object], T]:
    result = row_class
    for key in ("parse_obj",):
        if hasattr(row_class, key):
            result = getattr(row_class, key)
            break
    return result


def parse_row(row_class: T, row):
    return get_row_parser(row_class=row_class)(row)
