"""Badge component."""

from dotreact.components.libs.chakra import ChakraComponent
from dotreact.vars import Var


class Badge(ChakraComponent):
    """A badge component."""

    tag = "Badge"

    # Variant of the badge ("solid" | "subtle" | "outline")
    variant: Var[str]

    # The color of the badge
    color_scheme: Var[str]
