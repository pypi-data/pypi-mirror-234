"""
the Hochfrequenz Bilanzierungsobjekt
"""
from datetime import datetime
from typing import Optional

from bo4e.bo.geschaeftsobjekt import Geschaeftsobjekt

from ibims.enum import BoTypErweitert


class Bilanzierung(Geschaeftsobjekt):
    """
    Bilanzierung is a business object used for balancing. This object is no BO4E standard and a complete go
    implementation can be found at
    https://github.com/Hochfrequenz/go-bo4e/blob/3414a1eac741542628df796d6beb43eaa27b0b3e/bo/bilanzierung.go
    """

    bo_typ: BoTypErweitert = BoTypErweitert.BILANZIERUNG  # type: ignore[assignment]

    bilanzierungsbeginn: datetime
    """
    inclusive start date of balancing
    """
    bilanzierungsende: datetime
    """
    exclusive end date of balancing
    """

    bilanzkreis: Optional[str] = None
