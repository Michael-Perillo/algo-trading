from __future__ import annotations

from pydantic import Field

from trading_bot_mvp.shared.model import FieldMap


class AccountFieldMap(FieldMap):
    """
    Strongly-typed mapping from Alpaca account fields to common account model fields.
    The keys are the common model field names, and the values are the Alpaca API field names.
    """

    mapping: dict[str, str] = Field(
        default_factory=lambda: {
            'id': 'id',
            'status': 'status',
            'currency': 'currency',
            'cash': 'cash',
            'equity': 'equity',
            'buying_power': 'buying_power',
            'created_at': 'created_at',
        }
    )


class PositionFieldMap(FieldMap):
    """
    Strongly-typed mapping from Alpaca position fields to common position model fields.
    The keys are the common model field names, and the values are the Alpaca API field names.
    """

    mapping: dict[str, str] = Field(
        default_factory=lambda: {
            'vendor_asset_id': 'asset_id',
            'symbol': 'symbol',
            'exchange': 'exchange',
            'asset_class': 'asset_class',
            'qty': 'qty',
            'qty_available': 'qty_available',
            'side': 'side',
            'avg_entry_price': 'avg_entry_price',
            'market_value': 'market_value',
            'cost_basis': 'cost_basis',
            'unrealized_pl': 'unrealized_pl',
            'unrealized_plpc': 'unrealized_plpc',
            'unrealized_intraday_pl': 'unrealized_intraday_pl',
            'unrealized_intraday_plpc': 'unrealized_intraday_plpc',
            'current_price': 'current_price',
            'lastday_price': 'lastday_price',
            'change_today': 'change_today',
            'asset_marginable': 'asset_marginable',
        }
    )
