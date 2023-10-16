from logging import getLogger
from typing import Any, Callable, Dict, List, Mapping, Optional
import typing

from reactivex import Observable, operators, compose
from reactivex.abc import ObserverBase, SchedulerBase
from reactivex.disposable import CompositeDisposable, Disposable

from ..events.message import make_sub_unsub_messages

from ..models import CryptodotcomResponseMessage
from ..connection.generic import EnhancedWebsocket
from ..events import MethodName
from ..messages.filters.kind import keep_channel_messages
from elm_framework_helpers.output import info_operator
from expression import curry_flip

logger = getLogger(__name__)


@curry_flip(1)
def channel_subscription(
    source: Observable[CryptodotcomResponseMessage],
    socket: EnhancedWebsocket,
    channel: str,
    unsubscribe_on_dispose: bool
) -> Observable[CryptodotcomResponseMessage]:
    def subscribe(observer: ObserverBase, scheduler: Optional[SchedulerBase] = None):
        subscription_message, unsubscription_message = make_sub_unsub_messages(channel)

        socket.send_message(subscription_message)

        def on_exit():
            if unsubscribe_on_dispose:
                # We may be disconnected
                try:
                    socket.send_message(unsubscription_message)
                except Exception:
                    pass

        return CompositeDisposable(
            source.subscribe(observer, scheduler=scheduler),
            Disposable(action=on_exit),
        )

    return Observable(subscribe)


def subscribe_to_channel(
    messages: Observable[CryptodotcomResponseMessage],
    channel: str,
    unsubscribe_on_dispose: bool = True
) -> Callable[[Observable[EnhancedWebsocket]], Observable[CryptodotcomResponseMessage]]:
    def socket_to_channel_messages(
        socket: EnhancedWebsocket,
    ) -> Observable[CryptodotcomResponseMessage]:
        return messages.pipe(
            keep_channel_messages(channel),
            channel_subscription(socket, channel, unsubscribe_on_dispose),
        )

    return compose(
        operators.map(socket_to_channel_messages),
        operators.switch_latest(),
    )
