
import dataclasses
from typing import Any, Optional


@dataclasses.dataclass
class OrderCreateRequest:
    client_order_id: str
    symbol: str
    type: str
    side: str
    amount: float
    price: Optional[float] = None
    params: Optional[dict[str, Any]] = None