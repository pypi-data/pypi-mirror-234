import dataclasses
from typing import Any, Callable, Optional, TYPE_CHECKING
from ..connection import wait_for_response
from ..models import (
    CryptodotcomResponseMessage,
    EnhancedWebsocket,
    CryptodotcomRequestMessage,
    EnhancedWebsocketBehaviorSubject,
)
from elm_framework_helpers.output import debug_operator
from reactivex import Observable, operators, disposable, just, throw
from ..events import MethodName
from ccxt import cryptocom
from reactivex.scheduler import NewThreadScheduler
from ..models.rest import OrderCreateRequest

if TYPE_CHECKING:
    from ..models.order import OrderDict

def order_confirmation(
    messages: Observable[CryptodotcomResponseMessage],
    order_id: str,
):
    def is_match(message: CryptodotcomResponseMessage) -> bool:
        try:
            # TODO we should probably not assume single order per message for the future
            return message.result["data"][0]["order_id"] == order_id
        except:
            return False

    return messages.pipe(
        operators.filter(is_match),
        operators.take(1),
        operators.map(lambda x: x.result["data"][0]), 
        operators.flat_map(
            lambda x: just(x) if x["status"] in ["ACTIVE", "FILLED"] else throw(x["status"])
        ),
        operators.timeout(4.0),
    )


def create_order_factory(
    messages: Observable[CryptodotcomResponseMessage],
    exchange: cryptocom,
    socket: EnhancedWebsocketBehaviorSubject,
) -> Callable[
    [OrderCreateRequest], Observable["OrderDict"]
]:
    """Factory for create order API call

    Args:
        messages (Observable[CryptodotcomResponseMessage]): All messages
        exchange (cryptocom): CCXT exchange
        socket (EnhancedWebsocketBehaviorSubject): Socket behavior subject

    Returns:
        Callable[ [OrderCreateRequest], Observable[OrderDict] ]: Arguments for the returned function are:
    """

    def create_order(
        order_details: OrderCreateRequest
    ):
        """Create order

        Args:
            symbol (str):
            type (str):
            side (str): buy or sell
            amount (float): amount
            price (Optional[float], optional): price. Defaults to None.
            params (_type_, optional): _description_. Defaults to None.

        Returns:
            dict: Order per CCXT style
        """
        params = order_details.params or {}
        market = exchange.market(order_details.symbol)
        uppercaseType = order_details.type.upper()
        instrument_name = market["id"]
        symbol, amount, price = order_details.symbol, order_details.amount, order_details.price
        request = {
            "instrument_name": instrument_name,
            "side": order_details.side.upper(),
            "type": uppercaseType,
            "quantity": exchange.amount_to_precision(symbol, amount),
        }
        client_order_id = order_details.client_order_id
        request["client_oid"] = client_order_id
        if (uppercaseType == "LIMIT") or (uppercaseType == "STOP_LIMIT"):
            request["price"] = exchange.price_to_precision(symbol, price)
        postOnly = exchange.safe_value(params, "postOnly", False)
        if postOnly:
            request["exec_inst"] = "POST_ONLY"

        def subscribe(observer, scheduler=None):
            scheduler = NewThreadScheduler()
            recorded_messages = messages.pipe(
                operators.filter(
                    lambda x: (
                        x.result.get("channel") == f"user.order.{instrument_name}"
                    )
                ),
                operators.replay(),
            )
            message_id, sender = socket.value.request_to_observable(
                CryptodotcomRequestMessage(MethodName.CREATE_ORDER, params=request)
            )
            answer_messages = messages.pipe(
                operators.filter(lambda x: x.method == MethodName.CREATE_ORDER.value),
                operators.replay()
            )
            answer_sub = answer_messages.connect(scheduler=scheduler)
            feed_sub = recorded_messages.connect(scheduler=scheduler)

            return disposable.CompositeDisposable(
                answer_sub,
                feed_sub,
                answer_messages.pipe(
                    wait_for_response(
                        message_id,
                        sender,
                        3.0,
                    ),
                    operators.flat_map(
                        lambda x: just(x.result) if x.code == 0 else throw(x.message)
                    ),
                    operators.flat_map(
                        lambda x: order_confirmation(
                            recorded_messages, x["order_id"]
                        )
                    ),
                ).subscribe(observer, scheduler=scheduler),
            )

        return Observable(subscribe)

    return create_order
