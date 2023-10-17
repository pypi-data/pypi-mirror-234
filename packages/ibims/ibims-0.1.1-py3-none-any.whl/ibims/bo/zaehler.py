"""
Extend BO Zaehler to hold information about the data acquisition method.
New BO ZaehlerGas to disambiguate between use case `Strom` and `Gas`.
"""
from datetime import datetime
from typing import Literal, Optional

from bo4e.bo.zaehler import Zaehler
from bo4e.com.zeitraum import Zeitraum
from bo4e.enum.geraetemerkmal import Geraetemerkmal
from bo4e.enum.netzebene import Netzebene
from pydantic import field_validator

from ibims.enum import Messwerterfassung, ZaehlerTypErweitert


class ZaehlerErweitert(Zaehler):
    """
    Extend `Zaehler` with `Messwerterfassung`
    """

    zaehlertyp: ZaehlerTypErweitert  # type: ignore[assignment]

    messwerterfassung: Messwerterfassung

    nachstes_ablesedatum: Optional[datetime] = None

    aktiver_zeitraum: Optional[Zeitraum] = None


class ZaehlerGas(ZaehlerErweitert):
    """
    Resolve some ambiguity of `Strom` and `Gas`
    """

    zaehlergroesse: Geraetemerkmal
    """
    Add information 'Zählergröße' for 'Gaszähler'.
    """

    druckniveau: Literal[Netzebene.ND, Netzebene.MD, Netzebene.HD]

    @field_validator("zaehlergroesse")
    @classmethod
    def validate_zaehlergroesse(cls, zaehlergroesse: Geraetemerkmal) -> Geraetemerkmal:
        """
        Thanks to the ambiguity in the bo4e model we need to check if the `Geraetemerkmal` is indeed a 'Zählergröße'.
        """
        if not zaehlergroesse.value.startswith("GAS_"):
            raise ValueError(f"Illegal value for 'zaehlergroesse': {zaehlergroesse}")
        return zaehlergroesse
