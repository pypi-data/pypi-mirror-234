from typing import Any, Callable, Optional
from ..connection import wait_for_response
from ..models import (
    CryptodotcomResponseMessage,
    CryptodotcomRequestMessage,
    EnhancedWebsocketBehaviorSubject,
)
from reactivex import Observable, operators, disposable, just, throw
from ..events import MethodName


def order_confirmation(
    messages: Observable[CryptodotcomResponseMessage],
    order_id: str,
    client_order_id: str,
):
    def is_match(message: CryptodotcomResponseMessage) -> bool:
        try:
            data = message.result["data"][0]
            if order_id and data["order_id"] != order_id:
                return False
            if client_order_id and data["client_oid"] !=  client_order_id:
                return False
            return data["status"] == "canceled"
        except:
            return False

    return messages.pipe(
        operators.filter(is_match),
        operators.take(1),
        operators.timeout(2.0),
    )


def cancel_order_factory(
    messages: Observable[CryptodotcomResponseMessage],
    socket: EnhancedWebsocketBehaviorSubject,
) -> Callable[[str, str | None, bool | None, bool | None], Observable[bool]]:
    """Factory for cancel order API call

    Args:
        messages (Observable[CryptodotcomResponseMessage]): All messages
        socket (EnhancedWebsocketBehaviorSubject): Socket behavior subject

    Returns:
        Callable[ [str], Observable[bool] ]:

        order_id: str,

    """

    def cancel_order(order_id: str="", client_order_id: str | None="", wait_for_confirmation=True, ignore_errors=True):
        if order_id:
            request = {"order_id": order_id}
        elif client_order_id:
            request = {"client_oid": client_order_id}
        else:
            return throw(ValueError('Either order_id or client_order_id is required'))

        def subscribe(observer, scheduler=None):
            recorded_messages = messages.pipe(
                operators.replay(),
            )

            sub = recorded_messages.connect(scheduler=scheduler)
            message_id, sender = socket.value.request_to_observable(
                CryptodotcomRequestMessage(MethodName.CANCEL_ORDER, params=request)
            )

            def on_cancel(x):
                if x.code != 0 and not ignore_errors:
                    return throw(x.message)
                return just(x.result)

            send_request = messages.pipe(
                wait_for_response(
                    message_id,
                    sender,
                    2.0,
                )
            )
            if wait_for_confirmation:
                successful_request = send_request.pipe(
                    operators.flat_map(on_cancel),
                    operators.flat_map(
                        lambda x: order_confirmation(recorded_messages, order_id, client_order_id or "")
                    ),
                    operators.catch(
                        lambda exc, _source: just(False)
                        if ignore_errors
                        else throw(exc)
                    ),
                )
            else:
                successful_request = send_request.pipe(operators.map(lambda _: True))

            return disposable.CompositeDisposable(
                sub,
                successful_request.subscribe(observer, scheduler=scheduler),
            )

        return Observable(subscribe)

    return cancel_order
