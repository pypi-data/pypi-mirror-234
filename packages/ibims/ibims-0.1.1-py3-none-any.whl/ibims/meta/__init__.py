"""
additional meta information for all BOs or COMponents
"""
from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class MetaDataMixin(BaseModel):
    """
    a mixin that adds metadata to business objects and/or components
    """

    creation_date: Optional[datetime] = None
