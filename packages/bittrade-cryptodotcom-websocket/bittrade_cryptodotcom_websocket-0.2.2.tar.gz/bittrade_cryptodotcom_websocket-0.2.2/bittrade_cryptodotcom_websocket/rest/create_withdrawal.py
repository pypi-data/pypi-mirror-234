import dataclasses
from logging import getLogger
from typing import Callable, Optional, cast
from reactivex import Observable, defer, operators, just


from ..connection import wait_for_response
from elm_framework_helpers.output import info_operator
from ..events import MethodName
from ..models import (
    CryptodotcomRequestMessage, CreateWithdrawalResponse
)
from ..models.rest import CreateWithdrawalRequest
from .http_factory_decorator import http_factory
logger = getLogger(__name__)

def map_create_withdrawal_response():
    return operators.map(
        lambda x: cast(CreateWithdrawalResponse, x["result"])
    )

@http_factory
def create_withdrawal_http_factory(request: CreateWithdrawalRequest):
    return CryptodotcomRequestMessage(MethodName.CREATE_WITHDRAWAL, params=dataclasses.asdict(request))