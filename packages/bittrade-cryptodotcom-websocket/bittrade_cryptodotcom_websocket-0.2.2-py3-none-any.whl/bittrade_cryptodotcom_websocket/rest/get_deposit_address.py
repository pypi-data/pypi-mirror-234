from typing import Literal
from ..connection import wait_for_response
from ..models import (
    CryptodotcomResponseMessage,
    EnhancedWebsocket,
    CryptodotcomRequestMessage,
)
from reactivex import Observable, operators, just, throw
from ..events import MethodName

from returns.curry import curry

from typing import Any, Callable, Optional
from ..connection import wait_for_response
from ..models import (
    CryptodotcomResponseMessage,
    EnhancedWebsocket,
    CryptodotcomRequestMessage,
    EnhancedWebsocketBehaviorSubject
)
from elm_framework_helpers.output import info_operator
from reactivex import Observable, operators, disposable, empty
from ..events import MethodName
from ccxt import cryptocom
from reactivex.scheduler import NewThreadScheduler

def get_deposit_address_factory(
    response_messages: Observable[CryptodotcomResponseMessage], socket: EnhancedWebsocketBehaviorSubject
) -> Callable[
    [str], Observable[list[dict]]
]:
    def get_deposit_address(
        currency: str,
    ):
        ws = socket.value
        return response_messages.pipe(
            wait_for_response(
                ws.send_message(
                    CryptodotcomRequestMessage(
                        MethodName.GET_DEPOSIT_ADDRESS, params={
                            "currency": currency,
                        }
                    )
                ),
                2.0,
            ),
            operators.map(lambda x: x['result']['deposit_address_list'])
        )


    return get_deposit_address
