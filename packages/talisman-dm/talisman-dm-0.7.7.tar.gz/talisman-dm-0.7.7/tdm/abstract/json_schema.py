from abc import abstractmethod
from typing import Any, Dict, Type, TypeVar

from pydantic import BaseModel

from .datamodel import AbstractTreeDocumentContent

_AbstractContentModel = TypeVar('_AbstractContentModel', bound='AbstractContentModel')


class AbstractContentModel(BaseModel):
    @abstractmethod
    def to_content(self) -> AbstractTreeDocumentContent:
        pass

    @classmethod
    @abstractmethod
    def build(cls: Type[_AbstractContentModel], doc: AbstractTreeDocumentContent) -> _AbstractContentModel:
        pass


class MetadataModel(BaseModel):
    def to_metadata(self) -> Dict[str, Any]:
        return self.dict(exclude_none=True)
