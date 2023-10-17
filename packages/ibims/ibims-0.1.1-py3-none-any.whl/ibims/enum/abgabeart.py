"""
New ENUM for concession fee type
"""

from bo4e.enum.strenum import StrEnum


class Abgabeart(StrEnum):
    """
    This AbgabeArt models the Konzessionsabgabentyp.
    It contains concessionfee types needed for concessionFee mapping.
    """

    # See https://github.com/Hochfrequenz/BO4E-dotnet/blob/main/BO4E/ENUM/AbgabeArt.cs

    KAS = "KAS"
    SA = "SA"
    SAS = "SAS"
    TA = "TA"
    TAS = "TAS"
    TK = "TK"
    TKS = "TKS"
    TS = "TS"
    TSS = "TSS"
