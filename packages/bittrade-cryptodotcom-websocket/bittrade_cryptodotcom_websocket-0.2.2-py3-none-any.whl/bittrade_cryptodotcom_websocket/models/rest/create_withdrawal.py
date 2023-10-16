
import dataclasses
from typing import Any, Optional
from decimal import Decimal

@dataclasses.dataclass
class CreateWithdrawalRequest:
    currency: str
    amount: Decimal
    address: str
    network_id: str
    client_wid: Optional[str] = None
    address_tag: Optional[str] = None

