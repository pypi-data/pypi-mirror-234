"""
Extend BO rechnung to hold more possible invoice types
"""
from typing import Optional

from bo4e.bo.rechnung import Rechnung

from ibims.com import RechnungspositionErweitert
from ibims.enum import RechnungstypErweitert


class RechnungErweitert(Rechnung):
    """
    replace enum Rechnungstyp mit RechnungstypErweitert and add attributes, which can be found in the
    go implementation
    https://github.com/Hochfrequenz/go-bo4e/blob/3414a1eac741542628df796d6beb43eaa27b0b3e/bo/rechnung.go
    """

    rechnungspositionen: Optional[list[RechnungspositionErweitert]] = None  # type: ignore[assignment]
    rechnungstyp: RechnungstypErweitert  # type: ignore[assignment]
    ist_selbstausgestellt: Optional[bool] = None
    ist_reverse_charge: Optional[bool] = None
