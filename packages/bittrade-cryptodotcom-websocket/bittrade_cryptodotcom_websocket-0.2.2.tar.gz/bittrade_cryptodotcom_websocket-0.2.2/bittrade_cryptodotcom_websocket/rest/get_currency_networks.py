from logging import getLogger
from typing import Callable, Optional, cast
from reactivex import Observable, defer, operators, just


from ..connection import wait_for_response
from elm_framework_helpers.output import info_operator
from ..events import MethodName
from ..models import (
    CryptodotcomRequestMessage,
    NetworkResponse, HttpResponse
)
from .http_factory_decorator import http_factory
logger = getLogger(__name__)

def map_currency_networks() -> NetworkResponse:
    return operators.map(
        lambda x: cast(NetworkResponse, x["result"])
    )

@http_factory
def get_currency_networks_http_factory():
    return CryptodotcomRequestMessage(MethodName.GET_CURRENCY_NETWORKS, params={})