from os import getenv
import requests
import reactivex
from reactivex.disposable import Disposable
from ..models import CryptodotcomRequestMessage
from logging import getLogger

USER_URL = getenv("CRYPTODOTCOM_HTTP_USER_URL", "https://api.crypto.com/exchange/v1")
MARKET_URL = getenv(
    "CRYPTODOTCOM_HTTP_MARKET_URL", "https://api.crypto.com/exchange/v1"
)

session = requests.Session()

logger = getLogger(__name__)


def prepare_request(message: CryptodotcomRequestMessage) -> requests.models.Request:
    # message's method is not typed as MethodName but it likely is so try and catch that case and stringify it
    try:
        method = message.method.value  # type: ignore
    except AttributeError:
        method = message.method
    is_private = method.startswith("private")
    base_url = USER_URL if is_private else MARKET_URL
    http_method = "POST" if is_private else "GET"
    kwargs = {}
    if is_private:
        kwargs["json"] = {
            "id": message.id,
            "method": method,
            "params": message.params,
            "nonce": message.nonce,
        }
    else:
        kwargs["params"] = message.params
    return requests.Request(http_method, f"{base_url}/{method}", **kwargs)


def send_request(request: requests.models.Request) -> reactivex.Observable:
    def subscribe(
        observer: reactivex.abc.ObserverBase,
        scheduler: reactivex.abc.SchedulerBase | None = None,
    ) -> reactivex.abc.DisposableBase:
        response = session.send(request.prepare())
        if response.ok:
            body = response.json()
            if body["code"] == 0:
                observer.on_next(body)
                observer.on_completed()
            else:
                observer.on_error(body)
        else:
            try:
                logger.error(
                    "Error with request %s; request was %s",
                    response.text,
                    response.request.body,
                )
                response.raise_for_status()
            except Exception as exc:
                observer.on_error(exc)
        return Disposable()

    return reactivex.Observable(subscribe)
