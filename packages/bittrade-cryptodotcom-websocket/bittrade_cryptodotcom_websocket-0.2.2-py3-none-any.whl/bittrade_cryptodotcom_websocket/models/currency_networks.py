from typing import TypedDict

class NetworkDetails(TypedDict):
    network_id: str
    withdrawal_fee: float
    withdraw_enabled: bool
    min_withdrawal_amount: float
    deposit_enabled: bool
    confirmation_required: int

class Network(TypedDict):
    full_name: str
    default_network: str
    network_list: list[NetworkDetails]

class NetworkResponse(TypedDict):
    update_time: int
    currency_map: dict[str, Network]