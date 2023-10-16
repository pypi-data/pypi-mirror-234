from typing import Any, Callable, Optional
from ..connection import wait_for_response
from ..models import (
    CryptodotcomResponseMessage,
    EnhancedWebsocket,
    CryptodotcomRequestMessage,
    EnhancedWebsocketBehaviorSubject
)
from reactivex import Observable, operators, disposable
from ..events import MethodName
from ccxt import cryptocom
from reactivex.scheduler import NewThreadScheduler

from returns.curry import curry


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
        operators.map(lambda x: (
            exchange.parse_order(x.result["data"][0])
        )),
    )


def create_order_factory(
    messages: Observable[CryptodotcomResponseMessage], exchange: cryptocom, socket: EnhancedWebsocketBehaviorSubject
) -> Callable[
    [str, str, str, float, Optional[float], Optional[Any]], Observable[dict[str, Any]]
]:
    def create_order(
        symbol: str,
        type: str,
        side: str,
        amount: float,
        price: Optional[float]=None,
        params=None,
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
        params = params or {}
        market = exchange.market(symbol)
        uppercaseType = type.upper()
        request = {
            "instrument_name": market["id"],
            "side": side.upper(),
            "type": uppercaseType,
            "quantity": exchange.amount_to_precision(symbol, amount),
        }
        if (uppercaseType == "LIMIT") or (uppercaseType == "STOP_LIMIT"):
            request["price"] = exchange.price_to_precision(symbol, price)
        postOnly = exchange.safe_value(params, "postOnly", False)
        if postOnly:
            request["exec_inst"] = "POST_ONLY"
            params = exchange.omit(params, ["postOnly"])

        def subscribe(observer, scheduler=None):
            ws = socket.value
            recorded_messages = messages.pipe(
                operators.filter(
                    lambda x: (
                        x.result.get("channel") == f'user.order.{market["id"]}'
                    )
                ),
                operators.replay(),
            )
            sub = recorded_messages.connect(scheduler=NewThreadScheduler())

            return disposable.CompositeDisposable(
                sub,
                messages.pipe(
                    wait_for_response(
                        ws.send_message(
                            CryptodotcomRequestMessage(
                                MethodName.CREATE_ORDER, params=request
                            )
                        ),
                        2.0,
                    ),
                    operators.flat_map(
                        lambda x: order_confirmation(
                            recorded_messages, exchange, x.result["order_id"]
                        )
                    ),
                ).subscribe(observer),
            )

        return Observable(subscribe)

    return create_order
