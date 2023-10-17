"""
Custom bo4e object, that was created for a migration project
"""

from datetime import datetime

from bo4e.com.com import COM


class ConcessionFee(COM):
    # https://github.com/Hochfrequenz/integrated-bo4e-migration-models/issues/7
    """
    The Concession Fee object was created during a migration project.
    It contains attributes needed for metering mapping.
    """

    market_location_id: str
    """market location id of powercloud db"""
    group: str | None = None
    """group of the concession fee (e.g. "TA")"""
    obis: str
    """obis code"""
    active_from: datetime
    """inclusive active_from"""
    active_until: datetime | None = None
    """exclusive active_until, None means it is still active"""
    ka: str | None = None
    """amount of concession fee"""
