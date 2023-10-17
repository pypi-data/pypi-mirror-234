"""
New COM to hold information about banking data
"""
from datetime import datetime
from typing import Optional

from bo4e.com.com import COM
from pydantic import constr, field_validator

from ibims.com.sepa_info import SepaInfo


class Bankverbindung(COM):
    """
    This component contains bank connection information.
    """

    # required attributes

    iban: Optional[constr(min_length=15, max_length=34)] = None  # type:ignore[valid-type]
    """
    The IBAN (International Bank Account Number) is structured as follows:
    # 2-digit: country code
    # 2-digit: check digits
    # up to 30-digit: account identification

    """
    # international variiert die Länge, länge(DE) = 22

    bic: Optional[str] = None
    """
    The BIC (Business Identifier Code) consists 8 or 11 alphanumeric characters, structured as follows:
    # 4-digit: bank code
    # 2-digit: country code
    # 2-digit: location code
    # 3-digit: branch office (optional)
    """

    # optional attributes
    gueltig_seit: Optional[datetime] = None
    """
    Inclusive date from which on the account information is valid
    """
    gueltig_bis: Optional[datetime] = None
    """
    Inclusive date till which on the account information is valid
    """
    bankname: Optional[str] = None  #: Name der Bank, z.b. 'Sparkasse Bremen'
    """
    Consists the name of the Bank.
    """
    sepa_info: Optional[SepaInfo] = None  #: Informationen über das SEPA-Mandant
    """
    contains an object of the SepaInfo class that contains details about the sepa mandates.
    """
    kontoinhaber: Optional[str] = None
    """
    contains the name of the account holder in the format 'firstname lastname'
    """
    ouid: int
    """
    contains the ouid that is need for the paymentMeans in the Customer Loader
    """

    # pylint:disable=unused-argument, no-self-argument
    @field_validator("iban")
    @classmethod
    def validate_iban_laenge(cls, iban: str) -> str:
        """
        validate the length of the iban.
        """
        return iban
        # validierung auf ländercod und sonst nur zahlen noch bauen.
        # vlaidierung der iban nach https://ibanvalidieren.de/verifikation.html noch einbauen
        # bzw. https://de.wikipedia.org/wiki/Internationale_Bankkontonummer#Zusammensetzung international.

    @field_validator("bic")
    @classmethod
    def validate_bic_laenge(cls, bic: str) -> str:
        """
        validate the length of the bic.
        """
        if len(bic) == 8 or len(bic) == 11:
            return bic
        raise ValueError("bic has not 8 or 11 characters.")

    # validierung auf alphanumerisch noch bauen
