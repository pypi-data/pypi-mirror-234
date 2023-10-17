"""
Extend COM Verbrauch to hold various more information
"""

from datetime import datetime
from decimal import Decimal
from typing import Optional

from bo4e.com.verbrauch import Verbrauch
from bo4e.enum.strenum import StrEnum

from ibims.enum import Messwertstatus


class AblesendeRolle(StrEnum):
    """
    Eine (Markt)Rolle, die Verbräuche abliest.
    """

    VNB = "VNB"  #: der verteilnetzbetreiber
    ENDKUNDE = "ENDKUNDE"  #: der Endkunde selbst
    VORIGER_LIEFERANT = "VORIGER_LIEFERANT"  #: der vorherige Lieferant hat einen Verbrauch mitgeteilt)
    MSB = "MSB"  #: der messstellenbetreiber
    SYSTEM = "SYSTEM"  #: wert ist eine vom system erstellte schätzung


class Ablesungsstatus(StrEnum):
    """
    State of the reading
    """

    GUELTIG = "GUELTIG"
    UNGUELTIG = "UNGUELTIG"
    ABGERECHNET = "ABGERECHNET"


class VerbrauchErweitert(Verbrauch):
    """
    enhance the consumption object
    """

    # see https://github.com/bo4e/BO4E-python/issues/443

    # optional attributes
    ablesegrund: Optional[str] = None
    """
    Reason why the counter is read
    """
    ablesebeschreibung: Optional[str] = None
    """
    Details to the reading
    """
    periodenverbrauch: Optional[Decimal] = None

    periodenverbrauch_ursprung: Optional[str] = None

    ableser: Optional[AblesendeRolle] = None
    """
    from whom is thew reading coming from
    """
    status: Optional[Ablesungsstatus] = None
    """
    reading status
    """
    energiegehalt_gas: Optional[Decimal] = None

    energiegehalt_gas_gueltig_von: Optional[datetime] = None
    """
    valid from date for the calorific amount (inclusive start)
    """
    energiegehalt_gas_gueltig_bis: Optional[datetime] = None
    """
    valid to date for the calorific amount (exclusive end)
    """

    umwandlungsfaktor_gas: Optional[Decimal] = None

    umwandlungsfaktor_gas_gueltig_von: Optional[datetime] = None
    """
    valid from date for the conversion factor (inclusive start)
    """
    umwandlungsfaktor_gas_gueltig_bis: Optional[datetime] = None
    """
    valid to date for the conversion factor (exclusive end)
    """
    messwertstatus: Optional[Messwertstatus] = None
    """
    the messwertstatus is the status of meter reading
    """

    def is_single_tariff(self) -> bool:
        """
        Returns true if the consumption is single tariff ("Eintarif")
        """
        return "1.8.0" in self.obis_kennzahl

    def is_high_tariff(self) -> bool:
        """
        Returns true if the consumption is high tariff (HT, "Hochtarif")
        """
        return "1.8.1" in self.obis_kennzahl

    def is_low_tariff(self) -> bool:
        """
        Returns true if the consumption is low tariff (NT, "Niedertarif")
        """
        return "1.8.2" in self.obis_kennzahl
