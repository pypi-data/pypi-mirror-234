"""
This module contains the base class
"""
import warnings
from inspect import currentframe, getframeinfo
from typing import Any, Optional, TypeVar

from bomf.model import Bo4eDataSet

Model = TypeVar("Model", bound=Bo4eDataSet)


class DataSetBaseModel(Bo4eDataSet):
    """
    This class serves as base class for all dataset classes in this module. The main purpose for now is to override
    the `construct` method such that it logs a warning if the construct method is used but proceeds normally.
    """

    @classmethod
    def model_construct(cls: type[Model], _fields_set: Optional[set[str]] = None, **values: Any) -> Model:
        """
        Method definition copied from pydantic `construct(...)` method.
        It only logs a warning if this method is used but proceeds normally.
        """
        current_frame = currentframe()
        assert current_frame is not None
        call_frame = current_frame.f_back
        assert call_frame is not None
        call_frame_info = getframeinfo(call_frame)

        # filepath = Path(call_frame_info.filename).relative_to(Path(__file__).parents[5])
        warning_msg = (
            "Avoid using construct on datasets."
            + f" Used in {call_frame_info.function}, {call_frame_info.filename}:{call_frame_info.lineno}"
        )
        warnings.warn(
            warning_msg,
            category=DeprecationWarning,
        )
        # raise DeprecationWarning(warning_msg)
        # Uncomment this raise statement if you want to crash your tests on unwanted construct statements in your code.
        return super(DataSetBaseModel, cls).model_construct.__func__(  # type:ignore[attr-defined]
            cls, _fields_set, **values
        )
