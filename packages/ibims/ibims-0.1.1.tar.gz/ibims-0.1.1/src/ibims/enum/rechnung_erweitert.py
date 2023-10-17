"""
Extension of the official bo4e rechnungstyp
"""

from bo4e.enum.strenum import StrEnum


class RechnungstypErweitert(StrEnum):
    """
    Abbildung verschiedener Rechnungstypen zur Kennzeichnung von Rechnungen.
    Die neu hinzugefügten Rechnungstypen können in der go Implementierung gefunden werden.
    """

    # pylint:disable=line-too-long
    # https://github.com/Hochfrequenz/go-bo4e/blob/3414a1eac741542628df796d6beb43eaa27b0b3e/enum/rechnungstyp/rechnungstyp.go

    ENDKUNDENRECHNUNG = "ENDKUNDENRECHNUNG"
    """Eine Rechnung vom Lieferanten an einen Endkunden über die Lieferung von Energie"""
    NETZNUTZUNGSRECHNUNG = "NETZNUTZUNGSRECHNUNG"
    """Eine Rechnung vom Netzbetreiber an den Netznutzer. (i.d.R. der Lieferant) über die Netznutzung."""
    MEHRMINDERMENGENRECHNUNG = "MEHRMINDERMENGENRECHNUNG"
    """ Eine Rechnung vom Netzbetreiber an den Netznutzer. (i.d.R. der Lieferant)
    zur Abrechnung von Mengen-Differenzen zwischen Bilanzierung und Messung."""
    MESSSTELLENBETRIEBSRECHNUNG = "MESSSTELLENBETRIEBSRECHNUNG"
    """Rechnung eines Messstellenbetreibers an den Messkunden."""
    BESCHAFFUNGSRECHNUNG = "BESCHAFFUNGSRECHNUNG"
    """Rechnungen zwischen einem  Händler und Einkäufer von Energie."""
    AUSGLEICHSENERGIERECHNUNG = "AUSGLEICHSENERGIERECHNUNG"
    """Rechnung an den Verursacher von Ausgleichsenergie."""
    TURNUSRECHNUNG = "TURNUSRECHNUNG"
    ABSCHLAGSRECHNUNG = "ABSCHLAGSRECHNUNG"
    ABSCHLUSSRECHNUNG = "ABSCHLUSSRECHNUNG"
    ZWISCHENRECHNUNG = "ZWISCHENRECHNUNG"
    INTEGRIERTE_13TE_RECHNUNG = "INTEGRIERTE_13TE_RECHNUNG"
    MONATSRECHNUNG = "MONATSRECHNUNG"
    ZUSAETZLICHE_13TE_RECHNUNG = "ZUSAETZLICHE_13TE_RECHNUNG"
