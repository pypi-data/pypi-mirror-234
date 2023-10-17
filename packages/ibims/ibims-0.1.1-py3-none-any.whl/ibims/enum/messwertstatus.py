"""
Messwertstatus enum
"""
from enum import StrEnum


class Messwertstatus(StrEnum):
    """
    The enum Messwertstatus contains the status of a meter reading. The go implementation of this enum
    can be found in
    https://github.com/Hochfrequenz/go-bo4e/blob/86a2948b99be591db84039ebaf61ca3dff9bb1b0/enum/messwertstatus/messwertstatus.go
    """

    ABGELESEN = "ABGELESEN"
    ERSATZWERT = "ERSATZWERT"
    VORLAEUFIGERWERT = "VORLAEUFIGERWERT"
    ANGABE_FUER_LIEFERSCHEIN = "ANGABE_FUER_LIEFERSCHEIN"
    VORSCHLAGSWERT = "VORSCHLAGSWERT"
    NICHT_VERWENDBAR = "NICHT_VERWENDBAR"
    PROGNOSEWERT = "PROGNOSEWERT"
    ENERGIEMENGESUMMIERT = "ENERGIEMENGESUMMIERT"
    FEHLT = "FEHLT"
