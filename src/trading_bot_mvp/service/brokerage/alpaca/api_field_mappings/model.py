from __future__ import annotations
from typing import Dict

from pydantic import BaseModel, Field
from trading_bot_mvp.shared.model import FieldMap


class AccountFieldMap(FieldMap):
    """
    Strongly-typed mapping from Alpaca account fields to common account model fields.
    The keys are the common model field names, and the values are the Alpaca API field names.
    """
    mapping: Dict[str, str] = Field(default_factory=lambda: {
        "id": "id",
        "status": "status",
        "currency": "currency",
        "cash": "cash",  # fixed: map 'cash' to 'cash'
        "equity": "equity",
        "buying_power": "buying_power",
        "created_at": "created_at",
    })
