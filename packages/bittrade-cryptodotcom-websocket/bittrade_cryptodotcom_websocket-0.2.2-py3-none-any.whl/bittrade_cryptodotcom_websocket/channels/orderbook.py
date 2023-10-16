import functools
from typing import Literal, cast
from reactivex import Observable, compose, operators

from ..models import CryptodotcomResponseMessage
from .subscribe import subscribe_to_channel
from ccxt import cryptocom
from elm_framework_helpers.ccxt.models.orderbook import Orderbook, OrderbookEntry

exchange = cryptocom()

TickerData = dict[str, str]


def to_order_book_data(symbol: str, message: CryptodotcomResponseMessage) -> Orderbook:
    """Order book ccxt style https://docs.ccxt.com/en/latest/manual.html#order-book-structure"""
    return cast(Orderbook, exchange.parse_order_book(message.result["data"][0], symbol))


def subscribe_order_book(
    pair: str,
    depth: Literal["10", "50"],
    messages: Observable[CryptodotcomResponseMessage],
):
    instrument = pair.replace("/", "_")  # in case we used common USDT/USD
    channel_name = f"book.{instrument}.{depth}"

    return compose(
        subscribe_to_channel(messages, channel_name),
        operators.map(functools.partial(to_order_book_data, pair)),
    )


__all__ = [
    "subscribe_order_book",
]
