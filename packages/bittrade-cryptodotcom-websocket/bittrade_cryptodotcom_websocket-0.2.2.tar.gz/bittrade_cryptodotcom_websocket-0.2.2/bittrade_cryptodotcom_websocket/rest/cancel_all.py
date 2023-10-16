from logging import getLogger
from typing import Any, Callable, Literal
import requests

from ccxt import cryptocom
from elm_framework_helpers.output import info_operator
from reactivex import Observable, disposable, empty, just, operators, throw
from reactivex.scheduler import NewThreadScheduler

from ..connection import wait_for_response, prepare_request, send_request
from ..events import MethodName
from ..models import (
    CryptodotcomRequestMessage,
    CryptodotcomResponseMessage,
    EnhancedWebsocketBehaviorSubject,
    OrderDict,
)

logger = getLogger(__name__)


def wait_for_no_orders(
    messages: Observable[list[OrderDict]],
):
    return messages.pipe(
        operators.filter(lambda x: bool(x)),
        operators.timeout(2.0),
        operators.catch(lambda _exc, source: just(False)),
        operators.map(lambda _x: True),
    )


def cancel_all_factory(
    response_messages: Observable[CryptodotcomResponseMessage],
    open_orders_messages: Observable[list[OrderDict]] | None,
    exchange: cryptocom,
    socket: EnhancedWebsocketBehaviorSubject,
) -> Callable[[str, Literal["limit", "trigger", "all"]], Observable[bool]]:
    """Cancel all factory

    :param: response_messages: The feed of messages that receive response to requests (identified via their id)
    :param: feed_messages: The feed of user messages; IMPORTANT these must be subscribed to user/orders or the cancel all will not be detected and will timeout. If not provided, the cancel all will be called but no check of success is performed
    """

    def cancel_all(
        symbol: str,
        type: Literal["limit", "trigger", "all"],
    ):
        uppercase_type = (type or "limit").upper()
        market_id = exchange.market(symbol)["id"]

        def subscribe(observer, scheduler=None):
            ws = socket.value
            if open_orders_messages:
                recorded_messages = open_orders_messages.pipe(
                    operators.replay(),
                )
                sub = recorded_messages.connect(scheduler=NewThreadScheduler())
            else:
                logger.warning(
                    "Cancel order called; open orders feed not provided, no check will be performed"
                )
                sub = disposable.Disposable()

            def check_should_wait(x: CryptodotcomResponseMessage) -> Observable[Any]:
                if open_orders_messages is None:
                    return empty()
                # 316 just means there was no active order, that's fine
                if x.code == 0:
                    return wait_for_no_orders(recorded_messages)
                if x.code == 316:
                    return just(True)
                return throw(Exception("Refused to cancel orders %s", x.result))

            message_id, sender = ws.request_to_observable(
                CryptodotcomRequestMessage(
                    MethodName.CANCEL_ALL,
                    params={
                        "instrument_name": market_id,
                        "type": uppercase_type,
                    },
                )
            )

            return disposable.CompositeDisposable(
                sub,
                response_messages.pipe(
                    wait_for_response(
                        message_id,
                        sender,
                        2.0,
                    ),
                    operators.flat_map(check_should_wait),
                ).subscribe(observer, scheduler=scheduler),
            )

        return Observable(subscribe)

    return cancel_all


def cancel_all_http_factory(
    add_token: Callable[[requests.models.Request], requests.models.Request]
):
    def cancel_all_http(
        pair: str, order_type: Literal["limit", "trigger", "all"]
    ) -> Observable:
        message = CryptodotcomRequestMessage(
            MethodName.CANCEL_ALL, {"instrument_name": pair, "type": order_type.upper()}
        )
        request = prepare_request(message)
        return send_request(add_token(request))

    return cancel_all_http
