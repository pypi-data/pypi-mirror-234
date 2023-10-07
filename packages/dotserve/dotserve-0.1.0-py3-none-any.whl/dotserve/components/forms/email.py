"""An email input component."""

from dotserve.components.forms.input import Input
from dotserve.vars import Var


class Email(Input):
    """An email input component."""

    # The type of input.
    type_: Var[str] = "email"  # type: ignore
