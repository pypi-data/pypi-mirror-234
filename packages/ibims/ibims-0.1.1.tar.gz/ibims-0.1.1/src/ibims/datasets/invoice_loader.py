"""
Contains the dataset for the invoice loader
"""
from typing import Optional

from bo4e.bo.marktlokation import Marktlokation
from bo4e.bo.marktteilnehmer import Marktteilnehmer
from bo4e.bo.vertrag import Vertrag

from ibims.bo import Bilanzierung, RechnungErweitert
from ibims.datasets import DataSetBaseModel
from ibims.targetmodels import TransaktionsdatenInvoices


class InvoiceLoaderDataSet(DataSetBaseModel):
    """
    This is a bo4e dat set that consists out of
    * a Marktlokation
    * a RechnungErweitert
    * a Marktteilnhemer
    * a Bilanzierung (which is only relevant for a memi)
    * a Vertrag (which is only relevant for a memi)
    """

    marktlokation: Marktlokation
    """
    The following attributes need to be filled for this DataSet:
    - lokationsadresse
    - marktlokations_id
    - sparte
    """

    rechnung_erweitert: RechnungErweitert
    """
    The following attributes need to be filled for this Dataset:
    - rechungstyp
    - rechungsnummer
    - rechungsdatum
    - faelligkeitsdatum
    - rechungsperiode
    - gesamtnetto
    - gesamtsteuer
    - gesamtbrutto, this value should be negative for self issued invoices
    - zuzahlen, this value should be negative for self issued invoices
    - rechnungspositionen, the values of the fields teilsumme_steuer and teilsumme_netto should be negative for
    self-issued invoices
    - steuerbetrag, the values of the fields basiswert and steuerwert should be negative for self issued invoices
    - ist_selbstausgestellt,
    - ist_reverse_charge
    """

    marktteilnehmer: Marktteilnehmer
    """
    The following attributes need to be filled for this DataSet:
    - name1 (organization)
    - partneradresse
    - rollencodenummer
    - rollencodetyp
    - ansprechoartner
    - sparte
    """

    bilanzierung: Optional[Bilanzierung] = None
    """
    The following attributes need to be filled for this DataSet:
    - bilanzierungsbeginn
    - bilanzierungsende
    """

    vertrag: Optional[Vertrag] = None
    """
    The following attributes need to be filled for this DataSet:
    - vertragskonditionen (only the field netznutzungsabbrechung is needed)
    """

    transaktionsdaten: TransaktionsdatenInvoices
    """
    The following attributes need to be filled for this DataSet:
    - sparte
    - pruefidentifikator
    - lieferrichtung
    - duplikat
    - referenznummer
    - datenaustauschreferenz
    - absender
    - empfaenger
    - nachrichtendatum
    - nachrichten_referenznummer
    """
