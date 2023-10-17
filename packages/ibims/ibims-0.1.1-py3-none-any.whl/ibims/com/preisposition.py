"""
New COM to hold information about different variations and reasons for account locks
"""

from bo4e.com.preisposition import Preisposition
from bo4e.enum.steuerkennzeichen import Steuerkennzeichen


class PreispositionErweitert(Preisposition):
    """
    Extension of the bo4e Preisposition with taxrate
    """

    steuersatz: Steuerkennzeichen
    """
    The taxrate is given as a enum
    """
