"""A password input component."""

from dotreact.components.forms.input import Input
from dotreact.vars import Var


class Password(Input):
    """A password input component."""

    # The type of input.
    type_: Var[str] = "password"  # type: ignore
