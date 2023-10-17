
def __format_exception(__exception: Exception):
    typename = str(type(__exception).__name__)
    body = str(__exception)
    result = f"{typename} : {body}"
    return result


def handle_exception(__exception_id: str, __exception: Exception):
    exception = __format_exception(__exception)
    message = f"{__exception_id}: {exception}"
    print(message)
    return None
