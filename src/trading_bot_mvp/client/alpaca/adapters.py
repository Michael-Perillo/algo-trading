from trading_bot_mvp.client.alpaca.trading_models import Account as AlpacaAccountResponse
from trading_bot_mvp.client.alpaca.trading_models import Position as AlpacaPosition
from trading_bot_mvp.service.data.bars_column_models import BarsColumnMapping
from trading_bot_mvp.shared.model import Account, Position


def account_from_alpaca(alpaca_account_response: AlpacaAccountResponse) -> Account:
    return Account(
        id=alpaca_account_response.id,
        status=alpaca_account_response.status,
        currency=alpaca_account_response.currency,
        cash=alpaca_account_response.cash,
        equity=alpaca_account_response.equity,
        buying_power=alpaca_account_response.buying_power,
        created_at=alpaca_account_response.created_at,
    )


def position_from_alpaca(alpaca_position: AlpacaPosition) -> Position:
    return Position(
        vendor_asset_id=alpaca_position.asset_id,
        symbol=alpaca_position.symbol,
        exchange=alpaca_position.exchange,
        asset_class=alpaca_position.asset_class,
        qty=alpaca_position.qty,
        qty_available=alpaca_position.qty_available,
        side=alpaca_position.side,
        avg_entry_price=alpaca_position.avg_entry_price,
        market_value=alpaca_position.market_value,
        cost_basis=alpaca_position.cost_basis,
        unrealized_pl=alpaca_position.unrealized_pl,
        unrealized_plpc=alpaca_position.unrealized_plpc,
        unrealized_intraday_pl=alpaca_position.unrealized_intraday_pl,
        unrealized_intraday_plpc=alpaca_position.unrealized_intraday_plpc,
        current_price=alpaca_position.current_price,
        change_today=alpaca_position.change_today,
        asset_marginable=alpaca_position.asset_marginable,
        lastday_price=alpaca_position.lastday_price,
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
