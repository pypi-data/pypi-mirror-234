"""
Custom bo4e object, that was created for a migration project
"""

from decimal import Decimal
from typing import Optional

from bo4e.com.com import COM
from bo4e.enum.mengeneinheit import Mengeneinheit


class Zaehlpunkt(COM):
    """
    The zaehlpunkt object was created during a migration project.
    It contains attributes needed for metering mapping.
    """

    periodenverbrauch_vorhersage: Decimal
    einheit_vorhersage: Mengeneinheit = Mengeneinheit.KWH
    zeitreihentyp: str = "Z21"
    kunden_wert: Decimal | None
    einheit_kunde: Optional[Mengeneinheit] = None
    grundzustaendiger: bool = True
