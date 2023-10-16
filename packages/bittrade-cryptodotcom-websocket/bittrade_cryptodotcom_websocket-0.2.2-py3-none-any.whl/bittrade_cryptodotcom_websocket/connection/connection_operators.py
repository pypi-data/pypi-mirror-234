from typing import Callable, List, Optional, Tuple, cast

from reactivex import compose, operators, Observable

from ..models import EnhancedWebsocket, WebsocketBundle, WebsocketStatusBundle
from ..models.message_types import WEBSOCKET_STATUS


ReadyMessage = Tuple[EnhancedWebsocket, bool]


def filter_socket_status_only() -> Callable[
    [Observable[WebsocketBundle]], Observable[WebsocketStatusBundle]
]:
    def is_status(x):
        return x[1] == WEBSOCKET_STATUS

    """Grab only messages related to the status of the websocket connection"""
    return compose(
        operators.filter(is_status),
        operators.map(lambda x: cast(WebsocketStatusBundle, x)),
    )


def map_socket_only() -> Callable[
    [Observable[WebsocketBundle | ReadyMessage]], Observable[EnhancedWebsocket]
]:
    """Returns an observable that represents the websocket only whenever emitted"""
    return operators.map(lambda x: x[0])
