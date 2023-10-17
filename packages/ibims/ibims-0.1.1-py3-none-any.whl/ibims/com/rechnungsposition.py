"""
extension of the official BO4E Rechnungsposition
"""

from typing import Optional

from bo4e.com.rechnungsposition import Rechnungsposition

from ibims.enum import BDEWArtikelnummerErweitert


class RechnungspositionErweitert(Rechnungsposition):
    """
    This class extend the com Rechnungsposition by replacing the enum BDEWArtikelnummer
    with BDEWArtikelNummerErweitert
    """

    artikelnummer: Optional[BDEWArtikelnummerErweitert] = None  # type: ignore[assignment]
