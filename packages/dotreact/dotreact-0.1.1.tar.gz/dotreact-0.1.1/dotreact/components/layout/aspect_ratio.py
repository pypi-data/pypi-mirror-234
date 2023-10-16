"""A AspectRatio component."""

from dotreact.components.libs.chakra import ChakraComponent
from dotreact.vars import Var


class AspectRatio(ChakraComponent):
    """AspectRatio component is used to embed responsive videos and maps, etc."""

    tag = "AspectRatio"

    # The aspect ratio of the Box
    ratio: Var[float]
