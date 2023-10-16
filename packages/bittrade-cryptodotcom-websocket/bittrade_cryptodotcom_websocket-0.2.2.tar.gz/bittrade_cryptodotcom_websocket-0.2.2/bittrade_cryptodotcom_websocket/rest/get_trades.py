from logging import getLogger
from typing import Callable, Optional
from reactivex import Observable, defer, operators, just
from ccxt import cryptocom


from ..connection import wait_for_response
from elm_framework_helpers.output import info_operator
from ..events import MethodName
from ..models import (
    CryptodotcomRequestMessage,
    CryptodotcomResponseMessage,
    EnhancedWebsocketBehaviorSubject,
    EnhancedWebsocket,
    Trade
)
from .http_factory_decorator import http_factory
logger = getLogger(__name__)


def get_trades_factory(response_messages: Observable[CryptodotcomResponseMessage], ws: EnhancedWebsocketBehaviorSubject):
    def get_trades(instrument_name: str, count: Optional[int] = 25):
        def get_trades_(*_) -> Observable[list[Trade]]:
            return ws.pipe(
                operators.filter(lambda x: bool(x)), # Ensure we have a websocket connection
                operators.timeout(5.0),
                operators.map(lambda socket: socket.request_to_observable(CryptodotcomRequestMessage(MethodName.GET_TRADES, params={
                    "instrument_name": instrument_name,
                    "count": count
                }))),
                operators.flat_map(lambda x: response_messages.pipe(
                    wait_for_response(
                        x[0], x[1],
                        2.0
                    )
                )),
                operators.map(lambda x: [Trade(**d) for d in x.result['data']]),
            )
        return defer(get_trades_)
    return get_trades


@http_factory
def get_trades_http(instrument_name: str, count: Optional[int] = 25):
    return CryptodotcomRequestMessage(MethodName.GET_TRADES, params={
        "instrument_name": instrument_name,
        "count": count
    })