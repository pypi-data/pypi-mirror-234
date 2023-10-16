"""A heading component."""

from dotreact.components.libs.chakra import ChakraComponent
from dotreact.vars import Var


class Heading(ChakraComponent):
    """A page heading."""

    tag = "Heading"

    # Override the tag. The default tag is `<h2>`.
    as_: Var[str]

    # "4xl" | "3xl" | "2xl" | "xl" | "lg" | "md" | "sm" | "xs"
    size: Var[str]
