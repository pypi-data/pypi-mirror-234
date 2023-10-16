"""An email input component."""

from dotreact.components.forms.input import Input
from dotreact.vars import Var


class Email(Input):
    """An email input component."""

    # The type of input.
    type_: Var[str] = "email"  # type: ignore
