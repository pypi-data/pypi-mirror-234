"""
Contains classes that describe the boneycomb data structure and provides the base Transaktionsdaten class
"""
from typing import Literal, Optional

from bo4e.enum.sparte import Sparte
from pydantic import BaseModel


class Transaktionsdaten(BaseModel):
    """
    This class collects the data in transaktionsdaten
    """

    migration_id: Optional[str] = None
    import_fuer_storno_adhoc: Literal["true", "false"]
    sparte: Sparte
    pruefidentifikator: str
    datenaustauschreferenz: str
    nachrichtendatum: str
    nachrichten_referenznummer: str
    absender: str
    empfaenger: str


class TransaktionsdatenQuantities(Transaktionsdaten):
    """
    This class adds additional data to the transaktionsdaten, which is needed for a energy amount
    """

    migration_id: Optional[str] = None
    dokumentennummer: str
    kategorie: str
    nachrichtenfunktion: str
    typ: str
    datumsformat: str


InvoiceManagerInvoiceStatus = Literal["received", "ignored", "declined", "cancelled", "accepted", "manual_decision"]


class TransaktionsdatenInvoices(Transaktionsdaten):
    """
    This class adds additional data to the transaktionsdaten, which is needed for an invoice
    """

    lieferrichtung: Optional[str] = None
    referenznummer: Optional[str] = None
    duplikat: Literal["true", "false"]
    status: InvoiceManagerInvoiceStatus
    # the boneycombs transaktionsdaten are (string,string) key value pairs
    # hence this is not a real boolean but two possible literal strings.
