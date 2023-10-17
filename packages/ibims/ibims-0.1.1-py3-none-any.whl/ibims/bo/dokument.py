"""
Create a generic reference to a document
"""
from datetime import datetime

from bo4e.bo.geschaeftsobjekt import Geschaeftsobjekt


class Dokument(Geschaeftsobjekt):
    """
    A generic document reference like for bills, order confirmations and cancellations
    """

    erstellungsdatum: datetime
    """
    when was the document created
    """
    has_been_sent: bool
    """
    true iff the document was sent to the customer
    """
    dokumentenname: str
    """
    name of the document
    """
    vorlagenname: str
    """
    template of a document
    """
