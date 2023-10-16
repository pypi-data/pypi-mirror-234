import functools
from typing import Any, Callable, ParamSpec, TypeVar, TypedDict, cast
import requests
from ..connection import prepare_request, send_request
from ..models import CryptodotcomRequestMessage, HttpResponse
from reactivex import Observable

P = ParamSpec("P")


# TODO this typing does not work, it does not allow us to define the sub type of the response's result
R = TypeVar("R", bound=HttpResponse)

def http_factory(fn: Callable[P, CryptodotcomRequestMessage]):
    @functools.wraps(fn)
    def factory(add_token: Callable[[requests.models.Request], requests.models.Request]):
        def inner(*args: P.args, **kwargs: P.kwargs):
            request = fn(*args, **kwargs)
            return cast(Observable[R], send_request(
                add_token(prepare_request(request))
            ))
        return inner
    return factory
