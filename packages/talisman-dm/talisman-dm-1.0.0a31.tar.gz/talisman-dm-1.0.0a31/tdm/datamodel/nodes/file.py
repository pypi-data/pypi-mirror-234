from dataclasses import dataclass
from typing import Optional

from tdm.abstract.datamodel import AbstractContentNode, BaseNodeMetadata
from tdm.abstract.json_schema import generate_model


@dataclass(frozen=True)
class FileNodeMetadata(BaseNodeMetadata):
    """
    File node metadata

    Attributes
    --------
    name:
        file name
    size:
        file size (bytes)
    """
    name: Optional[str] = None
    size: Optional[int] = None


@generate_model(label='file')
@dataclass(frozen=True)
class FileNode(AbstractContentNode[FileNodeMetadata, str]):
    """
    Node for file representation.
    ``content`` contains file URI.
    """
    pass


@dataclass(frozen=True)
class ImageNodeMetadata(FileNodeMetadata):
    """
    Image node metadata

    Attributes
    --------
    width:
        image width
    height:
        image height
    """
    width: Optional[int] = None
    height: Optional[int] = None


@generate_model(label='image')
@dataclass(frozen=True)
class ImageNode(AbstractContentNode[ImageNodeMetadata, str]):
    """
    Node for image representation.
    ``content`` contains image file URI.
    """
    pass
