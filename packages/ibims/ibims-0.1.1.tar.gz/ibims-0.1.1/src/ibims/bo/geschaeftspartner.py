"""
Extend BO Geschäftspartner to hold various more information.
"""
from datetime import datetime
from typing import Optional

from bo4e.bo.geschaeftspartner import Geschaeftspartner


class GeschaeftspartnerErweitert(Geschaeftspartner):
    """
    enhance the businesspartner object
    """

    # see https://github.com/bo4e/BO4E-python/issues/443

    # optional attributes
    erstellungsdatum: Optional[datetime] = None
    """
    when was the businesspartner created
    """
    geburtstag: Optional[datetime] = None
    """
    When was the Business Partner born
    """
    telefonnummer_mobil: Optional[str] = None
    """
    Telephone-number for communications
    """
    telefonnummer_privat: Optional[str] = None
    """
    Telephone number for communications (landline)
    """
    telefonnummer_geschaeft: Optional[str] = None
    """
    Telephone number if the customer has a business
    """
    firmenname: Optional[str] = None
    """
    The name of the company if the GeschaeftspartnerErweitert represents an company
    """
    # added firmenname because name1, name2, name3 are already for surname, firstname and title
    # don't use gewerbekennzeichnung for mapping logic of company name,
    # because in database the company name is not filled all the time.

    hausbesitzer: Optional[bool] = None
    """
    Flag if the bussinespartner is the House owner.
    It is None if the Flag is not set by any reason
    """
