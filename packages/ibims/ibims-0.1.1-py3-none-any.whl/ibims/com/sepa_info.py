"""
New COM for holding information about sepa mandates
"""
from datetime import datetime
from typing import Optional

from bo4e.com.com import COM


class SepaInfo(COM):
    """
    This class includes details about the sepa mandates.
    """

    # required attributes

    sepa_id: str
    """
    System internal id of the SEPA mandate.
    """
    # muss noch überprüft werden wie es allgemeingültig umzusetzen ist.

    sepa_zahler: bool
    """
    there may be sepa information regardless of whether it is used or not. this field
    confirms the use case e.g. it is false if the customer pays for himself
    """

    # optional attributes
    creditor_identifier: Optional[str] = None
    """
    Creditor Identifier is a number that identify the creditor of the sepa transaction
    """

    gueltig_seit: Optional[datetime] = None
    """
    Inklusiver Zeitpunkt ab dem das SEPA Mandat gültig ist.
    """
