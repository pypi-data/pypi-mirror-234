from typing import Any, Callable, Literal, Optional

from ..connection import wait_for_response, prepare_request, send_request
from ..models import (
    CryptodotcomResponseMessage,
    CryptodotcomRequestMessage,
    EnhancedWebsocketBehaviorSubject,
)
from reactivex import Observable, operators
from ..events import MethodName
from ccxt import cryptocom
import requests


def order_confirmation(
    messages: Observable[CryptodotcomResponseMessage],
    exchange: cryptocom,
    order_id: str,
):
    def is_match(message: CryptodotcomResponseMessage) -> bool:
        try:
            return message.result["data"][0]["order_id"] == order_id
        except:
            return False

    return messages.pipe(
        operators.filter(is_match),
        operators.map(lambda x: (exchange.parse_order(x.result["data"][0]))),
    )


def close_position_factory(
    messages: Observable[CryptodotcomResponseMessage],
    exchange: cryptocom,
    socket: EnhancedWebsocketBehaviorSubject,
) -> Callable[[str, Literal["market", "limit"], Optional[str]], Observable]:
    def close_position(
        symbol: str, type: Literal["market", "limit"], price: Optional[str] = ""
    ):
        uppercase_type = type.upper()
        request = {"instrument_name": symbol, "type": uppercase_type}
        if (uppercase_type == "LIMIT") or (uppercase_type == "STOP_LIMIT"):
            request["price"] = exchange.price_to_precision(symbol, price)

        def subscribe(observer, scheduler=None):
            message_id, sender = socket.value.request_to_observable(
                CryptodotcomRequestMessage(
                    MethodName.CLOSE_POSITION,
                    params=request,
                )
            )
            return messages.pipe(
                wait_for_response(
                    message_id,
                    sender,
                    2.0,
                )
            ).subscribe(observer, scheduler=scheduler)

        return Observable(subscribe)

    return close_position


def close_position_http_factory(
    add_token: Callable[[requests.models.Request], requests.models.Request]
):
    def close_position_http(
        pair: str, order_type: Literal["limit", "market"], price: str | None = ""
    ) -> Observable:
        params = {"instrument_name": pair, "type": order_type.upper()}
        if price:
            params["price"] = price
        message = CryptodotcomRequestMessage(MethodName.CLOSE_POSITION, params)
        request = prepare_request(message)
        return send_request(add_token(request))

    return close_position_http
