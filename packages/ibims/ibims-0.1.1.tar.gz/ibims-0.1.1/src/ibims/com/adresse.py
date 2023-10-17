"""
extension for the official bo4e adresse
"""

from typing import Optional

from bo4e.com.adresse import Adresse


class AdresseErweitert(Adresse):
    """
    Extend Adresse with attribute ortsteil
    """

    ortsteil: Optional[str] = None
