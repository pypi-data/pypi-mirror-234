"""
New ENUM to differentiate the data acquisition method in BO Zähler.
"""
from bo4e.enum.strenum import StrEnum


class Messwerterfassung(StrEnum):
    """
    Specify data acquisition method
    """

    # https://github.com/bo4e/BO4E-python/issues/575

    FERNAUSLESBAR = "FERNAUSLESBAR"
    MANUELL_AUSGELESENE = "MANUELL_AUSGELESENE"
