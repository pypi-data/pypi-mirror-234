from dataclasses import dataclass

from tdm.abstract.datamodel import AbstractNodeMention
from tdm.abstract.json_schema import generate_model
from tdm.datamodel.nodes import ImageNode


@generate_model
@dataclass(frozen=True)
class ImageNodeMention(AbstractNodeMention):
    """
    Represents bounding box image node mention.

    Attributes
    --------
    node:
        The image node being mentioned.
    top:
        The top position of the bounding box.
    bottom:
        The bottom position of the bounding box.
    left:
        The left position of the bounding box.
    right:
         The right position of the bounding box.
    """
    node: ImageNode
    top: int
    bottom: int
    left: int
    right: int

    def __post_init__(self):
        if not isinstance(self.node, ImageNode):
            raise ValueError(f"Incorrect node type {type(self.node)}. Expected {ImageNode}")
        if self.top < 0 or self.bottom <= self.top or self.left < 0 or self.right <= self.left:
            raise ValueError(f"Incorrect bbox [({self.top}, {self.left}); ({self.bottom}, {self.right})]")
        if self.node.metadata.width is not None and self.right > self.node.metadata.width:
            raise ValueError(f"Bbox spreads out of the image (image width: {self.node.metadata.width})")
        if self.node.metadata.height is not None and self.bottom > self.node.metadata.height:
            raise ValueError(f"Bbox spreads out of the image (image height: {self.node.metadata.height})")
