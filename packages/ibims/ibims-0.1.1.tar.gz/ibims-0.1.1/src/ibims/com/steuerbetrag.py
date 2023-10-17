"""
Extension of the official steuerbetrag
"""
from decimal import Decimal
from typing import Optional

from bo4e.com.steuerbetrag import Steuerbetrag


class SteuerbetragErweitert(Steuerbetrag):
    """
    This class extends the com Steuerbetrag with the attribute steuerwert_vorausgezahlt, which can also be found in the
    go implementation:
    https://github.com/Hochfrequenz/go-bo4e/blob/8dda93f8eda51557bb355a93e94c379111f0242b/com/steuerbetrag.go
    """

    steuerwert_vorausgezahlt: Optional[Decimal] = None  #: tax amount of the prepaid amounts
