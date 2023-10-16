from decimal import Decimal
from typing import Callable, NamedTuple
from ..operators import extract_data
from ..connection.http import prepare_request, send_request
from ..models import (
    CryptodotcomRequestMessage,
    RawOrderbook,
    CryptodotcomResponseMessage,
    TopPrices,
)
from reactivex import operators, compose, Observable
from elm_framework_helpers.operators import item_at_index


def get_book_http(instrument_name: str, depth: int = 10):
    return send_request(
        prepare_request(
            CryptodotcomRequestMessage(
                "public/get-book", {"instrument_name": instrument_name, "depth": depth}
            )
        )
    )


def map_to_raw_orderbook() -> Callable[[Observable[dict]], Observable[RawOrderbook]]:
    return compose(
        operators.map(lambda x: CryptodotcomResponseMessage(**x)),
        extract_data(),
        item_at_index(0),
    )


def map_top_prices() -> Callable[[Observable[dict]], Observable[TopPrices]]:
    def map_top_prices_(x: RawOrderbook):
        return TopPrices(Decimal(x["bids"][0][0]), Decimal(x["asks"][0][0]))

    return compose(map_to_raw_orderbook(), operators.map(map_top_prices_))
