"""
Create a generic reference to a file object
"""
from typing import Optional

from pydantic import BaseModel


class File(BaseModel):
    """
    This class represents a file that is stored in the database.
    """

    file_name_for_docstore: Optional[str] = None
    """
    The name of the file in the docstore
    """

    folder_name_for_docstore: Optional[str] = None
    """
    The folder name of the file in the docstore
    """

    file: bytes
    """
    The body of the file
    """
