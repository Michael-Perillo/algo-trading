from collections.abc import Callable
from typing import Any, TypeVar

from pandas import to_datetime

from client.alpaca.generated.alpaca_trading.models.account import (
    Account as AlpacaAccountResponse,
)
from client.alpaca.generated.alpaca_trading.models.position import (
    Position as AlpacaPosition,
)
from client.alpaca.generated.alpaca_trading.types import UNSET
from service.data.bars_column_models import BarsColumnMapping
from shared.model import Account, Position, Side

T = TypeVar('T')


# fixme could just update the models to use the UNSET type
def parse_unset(value: Any, default: T, cast: Callable[[Any], T]) -> T:
    """
    Utility to handle Alpaca UNSET/None values with optional casting.
    :param value: The value to check.
    :param default: The default to return if value is None or UNSET.
    :param cast: Optional callable to cast the value if set.
    """
    if value in (None, UNSET):
        return default
    return cast(value)


def account_from_alpaca(alpaca_account_response: AlpacaAccountResponse) -> Account:
    return Account(
        id=alpaca_account_response.id,
        status=alpaca_account_response.status,
        currency=parse_unset(alpaca_account_response.currency, default='', cast=str),
        cash=parse_unset(alpaca_account_response.cash, default=0.0, cast=float),
        equity=parse_unset(alpaca_account_response.equity, default=0.0, cast=float),
        buying_power=parse_unset(alpaca_account_response.buying_power, default=0.0, cast=float),
        created_at=parse_unset(alpaca_account_response.created_at, default=None, cast=to_datetime),
    )


def position_from_alpaca(alpaca_position: AlpacaPosition) -> Position:
    return Position(
        vendor_asset_id=alpaca_position.asset_id,
        symbol=alpaca_position.symbol,
        exchange=alpaca_position.exchange,
        asset_class=alpaca_position.asset_class,
        qty=float(alpaca_position.qty),
        qty_available=parse_unset(alpaca_position.qty_available, default=None, cast=float),
        side=Side(alpaca_position.side),
        avg_entry_price=float(alpaca_position.avg_entry_price),
        market_value=float(alpaca_position.market_value),
        cost_basis=parse_unset(alpaca_position.cost_basis, default=None, cast=float),
        unrealized_pl=float(alpaca_position.unrealized_pl),
        unrealized_plpc=parse_unset(alpaca_position.unrealized_plpc, default=None, cast=float),
        unrealized_intraday_pl=parse_unset(
            alpaca_position.unrealized_intraday_pl, default=None, cast=float
        ),
        unrealized_intraday_plpc=parse_unset(
            alpaca_position.unrealized_intraday_plpc, default=None, cast=float
        ),
        current_price=parse_unset(alpaca_position.current_price, default=None, cast=float),
        change_today=parse_unset(alpaca_position.change_today, default=None, cast=float),
        asset_marginable=parse_unset(alpaca_position.asset_marginable, default=None, cast=bool),
        lastday_price=parse_unset(alpaca_position.lastday_price, default=None, cast=float),
    )


def alpaca_bars_column_mapping() -> BarsColumnMapping:
    # uses the values from the Alpaca StockBar model
    return BarsColumnMapping(
        timestamp='t',
        open='o',
        high='h',
        low='l',
        close='c',
        volume='v',
        # this one is not in the model, but we need it for the standardization
        symbol='symbol',
    )
