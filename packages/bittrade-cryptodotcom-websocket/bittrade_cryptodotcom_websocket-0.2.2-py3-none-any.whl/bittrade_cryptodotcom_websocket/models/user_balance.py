from pydantic.dataclasses import dataclass

@dataclass
class PositionBalance():
    instrument_name: str
    quantity: str
    market_value: str
    collateral_amount: str
    collateral_weight: str
    max_withdrawal_balance: str
    reserved_qty: str

@dataclass
class UserBalance():
    total_available_balance: str
    total_margin_balance: str
    total_initial_margin: str
    total_maintenance_margin: str
    total_position_cost: str
    total_cash_balance: str
    total_collateral_value: str
    total_session_unrealized_pnl: str
    instrument_name: str
    total_session_realized_pnl: str
    is_liquidating: bool
    total_effective_leverage: str
    position_limit: str
    used_position_limit: str
    position_balances: list[PositionBalance]