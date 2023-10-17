"""
Extension of the official BO4E Zaehlertyp
"""
from bo4e.enum.strenum import StrEnum


class ZaehlerTypErweitert(StrEnum):
    """Extension of the official BO4E Zaehlertyp"""

    DREHSTROMZAEHLER = "DREHSTROMZAEHLER"  #: Drehstromzaehler,

    BALGENGASZAEHLER = "BALGENGASZAEHLER"  #: Balgengaszähler,

    DREHKOLBENZAEHLER = "DREHKOLBENZAEHLER"  #: Drehkolbengaszähler,

    SMARTMETER = "SMARTMETER"  #: Smart Meter Zähler,

    LEISTUNGSZAEHLER = "LEISTUNGSZAEHLER"  #: leistungsmessender Zähler,

    MAXIMUMZAEHLER = "MAXIMUMZAEHLER"  #: Maximumzähler,

    TURBINENRADGASZAEHLER = "TURBINENRADGASZAEHLER"  #: Turbinenradgaszähler,

    ULTRASCHALLGASZAEHLER = "ULTRASCHALLGASZAEHLER"  #: Ultraschallgaszähler,

    WECHSELSTROMZAEHLER = "WECHSELSTROMZAEHLER"  #: Wechselstromzähler,

    WIRBELGASZAEHLER = "WIRBELGASZAEHLER"  #: Wirbelgaszähler,

    MESSDATENREGISTRIERGERAET = "MESSDATENREGISTRIERGERAET"  #: Messdatenregistriergerät,

    ELEKTRONISCHERHAUSHALTSZAEHLER = "ELEKTRONISCHERHAUSHALTSZAEHLER"  #: elektronischer Haushaltszähler,

    SONDERAUSSTATTUNG = "SONDERAUSSTATTUNG"  #: Individuelle Abstimmung (Sonderausstattung),

    MODERNEMESSEINRICHTUNG = "MODERNEMESSEINRICHTUNG"  #: moderne Messeinrichtung nach MsbG

    LASTGANGZAEHLER = "LASTGANGZAEHLER"  #: Lastgangzähler

    NEUEMESSEINRICHTUNG = "NEUEMESSEINRICHTUNG"  #: Neue Messeinrichtung GAS nach MsbG
    # https://github.com/bo4e/BO4E-python/issues/574
