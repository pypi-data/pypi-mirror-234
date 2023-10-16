import enum


class MethodName(str, enum.Enum):
    AUTHENTICATE = "public/auth"
    CANCEL_ALL = "private/cancel-all-orders"
    CANCEL_ORDER = "private/cancel-order"
    CLOSE_POSITION = "private/close-position"
    CREATE_ORDER = "private/create-order"
    CREATE_WITHDRAWAL = "private/create-withdrawal"
    GET_CURRENCY_NETWORKS = "private/get-currency-networks"
    GET_DEPOSIT_ADDRESS = "private/get-deposit-address"
    GET_OPEN_ORDERS = "private/get-open-orders"
    GET_POSITIONS = "private/get-positions"
    GET_TRADES = "public/get-trades"
    USER_GET_TRADES = "private/get-trades"
    SUBSCRIBE = "subscribe"
    UNSUBSCRIBE = "unsubscribe"
    USER_BALANCE = "private/user-balance"


__all__ = [
    "MethodName",
]
