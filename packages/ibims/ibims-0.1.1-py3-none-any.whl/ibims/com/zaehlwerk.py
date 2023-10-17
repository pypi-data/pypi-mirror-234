"""
Extend COM Zählwerk to hold various more information
"""

from datetime import datetime
from typing import Optional

from bo4e.com.zaehlwerk import Zaehlwerk

from ibims.enum import Abgabeart


class ZaehlwerkErweitert(Zaehlwerk):
    """
    enhance the register object
    """

    # see https://github.com/bo4e/BO4E-python/issues/443

    # optional attributes
    vorkommastellen: int
    """
    Integer places of the register
    """
    nachkommastellen: int
    """
    Decimal places of the register
    """
    schwachlastfaehig: bool

    konzessionsabgaben_typ: Optional[Abgabeart] = None

    active_from: datetime

    active_until: Optional[datetime] = None

    description: Optional[str] = None

    verbrauchsart: Optional[str] = None
