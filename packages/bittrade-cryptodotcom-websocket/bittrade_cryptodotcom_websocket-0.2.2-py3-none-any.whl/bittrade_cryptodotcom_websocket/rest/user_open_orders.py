from typing import Optional, cast
from reactivex import Observable, operators
from ccxt import cryptocom

from bittrade_cryptodotcom_websocket.connection import wait_for_response
from bittrade_cryptodotcom_websocket.events import MethodName
from bittrade_cryptodotcom_websocket.models import (
    CryptodotcomRequestMessage,
    CryptodotcomResponseMessage,
    EnhancedWebsocketBehaviorSubject,
    OrderDict,
)
from bittrade_cryptodotcom_websocket.operators.stream.response_messages import extract_data


def to_open_orders_entries(exchange: cryptocom):
    def to_open_orders_entries_(message: CryptodotcomResponseMessage):
        return cast(list[dict], exchange.parse_orders(message.result["data"]))

    return to_open_orders_entries_


def get_user_open_orders_factory(
    messages: Observable[CryptodotcomResponseMessage],
    socket: EnhancedWebsocketBehaviorSubject,
):
    def get_user_open_orders(
        instrument: Optional[str] = "",
    ) -> Observable[list[OrderDict]]:
        params = {"instrument_name": instrument} if instrument else {}
        message_id, sender = socket.value.request_to_observable(CryptodotcomRequestMessage(
            MethodName.GET_OPEN_ORDERS, params=params
        ))
        return messages.pipe(
            wait_for_response(
                message_id, sender
            ),
            extract_data(),
        )

    return get_user_open_orders
