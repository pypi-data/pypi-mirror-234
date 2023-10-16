from typing import Callable
from reactivex import Observable, compose, operators
from ...models import CryptodotcomResponseMessage


def keep_response_messages_only():
    def is_response(x: CryptodotcomResponseMessage):
        return x.id != -1

    return operators.filter(is_response)


def exclude_response_messages():
    def is_response(x: CryptodotcomResponseMessage):
        return x.id == -1

    return operators.filter(is_response)


def extract_data() -> Callable[
    [Observable[CryptodotcomResponseMessage]], Observable[list | dict]
]:
    return operators.map(lambda x: x.result["data"])
