from logging import getLogger
from typing import Callable
from ccxt import cryptocom
from reactivex import Observable, defer, operators, just

from ..connection import wait_for_response
from elm_framework_helpers.output import info_operator
from ..events import MethodName
from ..models import (
    CryptodotcomRequestMessage,
    CryptodotcomResponseMessage,
    EnhancedWebsocketBehaviorSubject,
    UserBalance,
)
logger = getLogger(__name__)


def get_user_balance_factory(response_messages: Observable[CryptodotcomResponseMessage], ws: EnhancedWebsocketBehaviorSubject):
    def get_user_balance():
        def get_user_balance_(*_) -> Observable[list[UserBalance]]:
            if not ws.value:
                logger.error('No websocket. You need to wait for the first ready and authenticated websocket (use concat or other)')
                return just([])
            message_id, sender = ws.value.request_to_observable(CryptodotcomRequestMessage(MethodName.USER_BALANCE))
            return response_messages.pipe(
                wait_for_response(
                    message_id, sender,
                    2.0
                ),
                operators.map(lambda x: [UserBalance(**d) for d in x.result['data']]),
            )
        return defer(get_user_balance_)
    return get_user_balance

def user_balance_for_instrument(instrument: str) -> Callable[[Observable[list[UserBalance]]], Observable[UserBalance | None]]:
    def find(x: list[UserBalance]):
        for d in x:
            if d.instrument_name == instrument:
                return d
    return operators.map(find)
