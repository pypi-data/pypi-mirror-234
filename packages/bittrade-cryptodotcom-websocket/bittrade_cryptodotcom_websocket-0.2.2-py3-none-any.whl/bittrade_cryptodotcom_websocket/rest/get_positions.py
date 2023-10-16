from ..connection import wait_for_response
from ..models import CryptodotcomResponseMessage, EnhancedWebsocket, CryptodotcomRequestMessage, EnhancedWebsocketBehaviorSubject
from reactivex import Observable
from ..events import MethodName
from ccxt import cryptocom


def get_positions_factory(response_messages: Observable[CryptodotcomResponseMessage], exchange: cryptocom, ws: EnhancedWebsocketBehaviorSubject):
    def get_positions(symbol: str):
        return response_messages.pipe(
            wait_for_response(
                ws.value.send_message(
                    CryptodotcomRequestMessage(MethodName.GET_POSITIONS, {
                        "instrument_name": exchange.market(symbol)['id']
                    })
                ),
                2.0
            )
        )
    return get_positions
