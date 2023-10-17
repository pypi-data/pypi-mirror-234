"""
Prognosegrundlage enum
"""
from enum import StrEnum


class Prognosegrundlage(StrEnum):
    """
    Prognosegrundlage describes the data used to perform a prognosis. This enum is not part of the official BO4E
    standard, but can be found the go and c# implementation:
    https://github.com/Hochfrequenz/go-bo4e/blob/main/enum/prognosegrundlage/prognosegrundlage.go
    https://github.com/Hochfrequenz/BO4E-dotnet/blob/main/BO4E/ENUM/Prognosegrundlage.cs
    """

    WERTE = "WERTE"
    PROFILE = "PROFILE"
