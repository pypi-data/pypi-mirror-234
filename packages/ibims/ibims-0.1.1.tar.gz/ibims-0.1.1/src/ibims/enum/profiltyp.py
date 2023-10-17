"""
Profiltyp enum
"""
from enum import StrEnum


class Profiltyp(StrEnum):
    """
    This enum specifies the forecast (Prognosegrundlage)
    """

    SLP_SEP = "SLP_SEP"
    """
    corresponds to Standardlastprofil/Standardeinspeiseprofile
    """
    TLP_TEP = "TLP_TEP"
    """
    corresponds to Tagesparameterabhängige Lastprofile/Einspeiserprofile
    """
