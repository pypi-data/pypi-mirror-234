from decimal import Decimal
from typing import NamedTuple, TypedDict

RawOrderbookEntry = tuple[str, str, str]
RawOrderbook = dict[str, list[RawOrderbookEntry | int]]


class OrderbookEntryNamedTuple(NamedTuple):
    price: Decimal
    quantity: Decimal
    number_of_orders: int


class OrderbookDict(TypedDict):
    bids: list[OrderbookEntryNamedTuple]
    asks: list[OrderbookEntryNamedTuple]
    t: int


class TopPrices(NamedTuple):
    bid: Decimal
    ask: Decimal
