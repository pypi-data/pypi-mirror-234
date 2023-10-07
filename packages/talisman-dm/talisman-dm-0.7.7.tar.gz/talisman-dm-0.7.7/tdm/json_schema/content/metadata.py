from typing import Dict, Optional

from pydantic import BaseModel, validator

from tdm.abstract.datamodel import NodeType
from tdm.datamodel import TreeDocumentContent


class NodeMetadata(BaseModel):
    node_type: NodeType
    original_text: Optional[str]
    text_translations: Dict[str, str] = {}
    language: Optional[str] = None
    hidden: bool = False

    class Config:
        extra = 'allow'  # any other extra fields will be kept

    def parse(self) -> dict:
        return self.dict()

    @validator('node_type', pre=True)
    def fix_incorrect_node_type(cls, value):  # noqa: N805
        try:
            return NodeType(value)
        except ValueError:
            return NodeType.TEXT

    @classmethod
    def build(cls, node: TreeDocumentContent) -> 'NodeMetadata':
        return cls.construct(
            node_type=node.type,
            original_text=node.original_node_text if node.original_node_text != node.node_text else None,
            text_translations={lang: node.get_node_text_translation(lang) for lang in node.node_text_languages},
            hidden=node.is_hidden,
            language=node.language
        )
