from typing import Callable, cast
from reactivex import Observable, compose, operators
from reactivex.operators import flat_map, with_latest_from
from ..models import (
    Order,
    CryptodotcomResponseMessage,
    EnhancedWebsocket,
    CryptodotcomRequestMessage,
    EnhancedWebsocketBehaviorSubject,
)


from ..rest import get_user_open_orders_factory

from ..operators.stream.response_messages import extract_data
from ..models import OrderDict

from .subscribe import subscribe_to_channel
from ccxt import cryptocom

OpenOrdersData = list[Order]


def _subscribe_open_orders(
    messages: Observable[CryptodotcomResponseMessage],
    instrument: str = "",
    unsubscribe_on_dispose: bool = True,
):
    instrument = instrument.replace("/", "_")
    channel = "user.order" + ("" if not instrument else f".{instrument}")
    return subscribe_to_channel(messages, channel, unsubscribe_on_dispose)


def to_open_orders_entries(exchange: cryptocom):
    def to_open_orders_entries_(message: CryptodotcomResponseMessage):
        return cast(list[dict], exchange.parse_orders(message))

    return to_open_orders_entries_


def subscribe_open_orders_reload(
    response_messages: Observable[CryptodotcomResponseMessage],
    feed_messages: Observable[CryptodotcomResponseMessage],
    socket: EnhancedWebsocketBehaviorSubject,
    exchange: cryptocom,
    symbol: str = "",
    unsubscribe_on_dispose: bool = True,
) -> Callable[[Observable[EnhancedWebsocket]], Observable[list[dict]]]:
    """Subscribe to open orders, but each time it emits (it emits updates only), we reload the actual open orders snapshot via RE

    Args:
        response_messages (Observable[CryptodotcomResponseMessage]): Feed of response messages aka messages with an id other than -1 which are responses to request
        feed_messages (Observable[CryptodotcomResponseMessage]): Feed of channel messages with id=-1
        socket (EnhancedWebsocketBehaviorSubject): Behavior subject holding the current
        exchange (cryptocom): CCXT exchange for symbol conversion etc
        symbol (str, optional): Pair to listen to. Defaults to "" in which case it includes all open orders.
        unsubscribe_on_dispose (bool, optional): Whether to send "unsubscribe" on dispose. This can be useful when other parts of the application want to use the feed, though this can be achieved by using the correct hot observable. Defaults to True.

    Returns:
        Callable[[Observable[EnhancedWebsocket]], Observable[list[dict]]]: Feed of open orders snapshots
    """
    instrument = ""
    if symbol:
        instrument = exchange.market(symbol)["id"]

    get_open_orders = get_user_open_orders_factory(response_messages, socket, exchange)

    def reload(_x) -> Observable:
        return get_open_orders(instrument)

    return compose(
        _subscribe_open_orders(feed_messages, instrument, unsubscribe_on_dispose),
        flat_map(reload),
        operators.map(to_open_orders_entries(exchange)),
    )


def subscribe_open_orders(
    all_messages: Observable[CryptodotcomResponseMessage],
    instrument: str = "",
    unsubscribe_on_dispose: bool = True,
) -> Callable[[Observable[EnhancedWebsocket]], Observable[list[OrderDict]]]:
    """Unparsed orders (only extracted result array)"""
    return compose(
        _subscribe_open_orders(all_messages, instrument, unsubscribe_on_dispose),
        extract_data(),  # type: ignore
    )


__all__ = ["subscribe_open_orders", "subscribe_open_orders_reload"]
