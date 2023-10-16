from typing import Callable, Dict, List, cast

from reactivex import Observable, compose, operators, timer


from ..connection.generic import WEBSOCKET_MESSAGE
from ..models.status import Status
from ..models import (
    CryptodotcomResponseMessage,
    EnhancedWebsocket,
    WebsocketBundle,
    WebsocketStatusBundle,
)


def _is_message(message: WebsocketBundle) -> bool:
    return message[1] == WEBSOCKET_MESSAGE


def message_only() -> Callable[
    [Observable[WebsocketBundle] | Observable[WebsocketStatusBundle]],
    Observable[Status | dict],
]:
    return operators.map(lambda x: x[2])


def keep_messages_only() -> Callable[
    [Observable[WebsocketBundle]], Observable[CryptodotcomResponseMessage]
]:
    return compose(
        operators.filter(_is_message),
        message_only(),
        operators.map(lambda x: CryptodotcomResponseMessage(**cast(dict, x))),
    )


def keep_new_socket_only() -> Callable[
    [Observable[WebsocketBundle]], Observable[EnhancedWebsocket]
]:
    def wait(x: EnhancedWebsocket):
        return timer(1.0).pipe(operators.map(lambda _: x))

    return compose(
        operators.map(lambda x: x[0]),
        operators.distinct_until_changed(),
        operators.map(wait),
        operators.switch_latest(),
    )
