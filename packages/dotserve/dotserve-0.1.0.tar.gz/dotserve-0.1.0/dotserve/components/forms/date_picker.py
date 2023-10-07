"""A date input component."""

from dotserve.components.forms.input import Input
from dotserve.vars import Var


class DatePicker(Input):
    """A date input component."""

    # The type of input.
    type_: Var[str] = "date"  # type: ignore
