"""
A Preisgarantie with MetaData added
"""
from typing import Optional

from bo4e.com.preisgarantie import Preisgarantie
from bo4e.enum.preisgarantietyp import Preisgarantietyp

from ibims.meta import MetaDataMixin


class PreisgarantieErweitert(Preisgarantie, MetaDataMixin):
    """
    eine Preisgarantie mit Metadaten
    """

    preisgarantietyp: Optional[Preisgarantietyp] = None  # type:ignore[assignment]
    """overrides the original preisgarantietyp with a nullable"""
