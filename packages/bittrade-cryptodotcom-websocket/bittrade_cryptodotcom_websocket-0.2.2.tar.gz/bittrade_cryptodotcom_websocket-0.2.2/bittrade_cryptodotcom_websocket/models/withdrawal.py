
from typing import TypedDict


class CreateWithdrawalResponse(TypedDict):
    id: int
    amount: float
    fee: float
    symbol: str
    address: str
    client_wid: str
    create_time: int
    network_id: str