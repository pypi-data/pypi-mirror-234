from typing import Callable
from reactivex import Observable, operators

from logging import getLogger
from typing import Callable, Optional, cast, TYPE_CHECKING

import requests
from ccxt import cryptocom
from reactivex import Observable, operators
from reactivex.disposable import CompositeDisposable
from reactivex.operators import flat_map, share
from reactivex.scheduler import ThreadPoolScheduler
from reactivex.subject import BehaviorSubject

from ..models import (
    CryptodotcomResponseMessage,
    EnhancedWebsocket,
    EnhancedWebsocketBehaviorSubject,
)

from ..operators import (
    exclude_response_messages,
    keep_messages_only,
    keep_new_socket_only,
    keep_response_messages_only,
)
from ..connection import (
    private_websocket_connection,
    public_websocket_connection,
)
from ..channels import (
    subscribe_open_orders,
    subscribe_order_book,
)
from ..rest import (
    cancel_all_factory,
    cancel_all_http_factory,
    cancel_order_factory,
    close_position_factory,
    close_position_http_factory,
    create_order_factory,
    create_withdrawal_http_factory,
    get_user_balance_factory,
    get_currency_networks_http_factory,
    get_user_open_orders_factory,
    get_user_trades_http,
    get_user_trades_factory,
)

from ..models import BookConfig, CryptodotcomContext


logger = getLogger(__name__)


def get_framework(
    add_token: Callable[
        [Observable[CryptodotcomResponseMessage]],
        Callable[[EnhancedWebsocket], Observable[EnhancedWebsocket]],
    ],
    add_token_http: Callable[[requests.models.Request], requests.models.Request],
    books: Optional[tuple[BookConfig]] = None,
    load_markets=True,
) -> CryptodotcomContext:
    books = books or cast(tuple[BookConfig], ())
    exchange = cryptocom()
    if load_markets:
        exchange.load_markets()
    pool_scheduler = ThreadPoolScheduler(200)
    all_subscriptions = CompositeDisposable()
    # Set up sockets
    public_sockets = public_websocket_connection()
    private_sockets = private_websocket_connection()

    public_messages = public_sockets.pipe(keep_messages_only(), share())
    private_messages = private_sockets.pipe(keep_messages_only(), share())

    authenticated_sockets = private_sockets.pipe(
        keep_new_socket_only(),
        flat_map(add_token(private_messages)),
        share(),
    )
    response_messages = private_messages.pipe(keep_response_messages_only(), share())
    feed_messages = private_messages.pipe(exclude_response_messages(), share())

    book_observables = {}
    for pair, depth in books or ():
        book_observables[f"{pair}_{depth}"] = public_sockets.pipe(
            keep_new_socket_only(),
            subscribe_order_book(pair, str(depth), public_messages),  # type: ignore
            share(),
        )

    socket_bs: EnhancedWebsocketBehaviorSubject = BehaviorSubject(
        cast(EnhancedWebsocket, None)
    )
    authenticated_sockets.subscribe(socket_bs)
    guaranteed_socket = socket_bs.pipe(
        operators.filter(lambda x: bool(x)),
    )
    get_user_open_orders = get_user_open_orders_factory(response_messages, socket_bs)
    open_orders = guaranteed_socket.pipe(
        subscribe_open_orders(private_messages), share()
    )
    open_orders_reloaded = open_orders.pipe(flat_map(lambda _: get_user_open_orders()))

    return CryptodotcomContext(
        all_subscriptions=all_subscriptions,
        books=book_observables,
        cancel_all=cancel_all_factory(
            response_messages, open_orders, exchange, socket_bs
        ),
        cancel_all_http=cancel_all_http_factory(add_token_http),
        cancel_order=cancel_order_factory(private_messages, socket_bs),
        close_position=close_position_factory(response_messages, exchange, socket_bs),
        close_position_http=close_position_http_factory(add_token_http),
        create_order=create_order_factory(private_messages, exchange, socket_bs),
        create_withdrawal_http=create_withdrawal_http_factory(add_token_http),
        exchange=exchange,
        feed_messages=feed_messages,
        get_currency_networks_http=get_currency_networks_http_factory(add_token_http),
        get_user_trades=get_user_trades_factory(response_messages, socket_bs),
        get_user_trades_http=get_user_trades_http(add_token_http),
        get_user_balance=get_user_balance_factory(response_messages, socket_bs),
        get_user_open_orders=get_user_open_orders,
        guaranteed_websocket=guaranteed_socket,
        open_orders_reloaded=open_orders_reloaded,
        open_orders=open_orders,
        private_messages=private_messages,
        public_messages=public_messages,
        public_socket_connection=public_sockets,
        private_socket_connection=private_sockets,
        response_messages=response_messages,
        scheduler=pool_scheduler,
        websocket_bs=socket_bs,
    )
