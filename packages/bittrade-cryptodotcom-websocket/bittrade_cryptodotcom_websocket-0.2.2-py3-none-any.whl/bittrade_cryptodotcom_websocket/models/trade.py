from dataclasses import dataclass
from typing import Literal

@dataclass
class Trade:
    s: Literal["SELL", "BUY"]
    p: str
    q: str
    t: int
    d: str
    i: str
