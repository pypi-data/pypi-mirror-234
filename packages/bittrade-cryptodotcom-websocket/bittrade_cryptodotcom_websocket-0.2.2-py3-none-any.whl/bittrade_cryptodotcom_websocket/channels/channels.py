import enum


class ChannelName(enum.Enum):
    CHANNEL_OHLC = "ohlc"
    CHANNEL_BOOK = "book"
    CHANNEL_SPREAD = "spread"
    CHANNEL_TICKER = "ticker"
    CHANNEL_TRADE = "trade"
    CHANNEL_OWN_TRADES = "ownTrades"
    CHANNEL_OPEN_ORDERS = "openOrders"
    PUBLIC_GET_BOOK = "public/get-book"


__all__ = [
    "ChannelName",
]
