from collections import defaultdict
from typing import Dict, Optional, Tuple, Union

from pydantic import BaseModel

from tdm.abstract.datamodel import AbstractFact, AbstractTalismanDocument, FactType
from tdm.datamodel import TalismanDocument
from .content import TreeDocumentContentModel
from .directive import CreateAccountDirectiveModel, CreateConceptDirectiveModel, CreatePlatformDirectiveModel, build_directive_model
from .fact import ConceptFactModel, PropertyFactModel, RelationFactModel, ValueFactModel, build_fact_model
from ..abstract.json_schema import MetadataModel

FactModel = Union[ConceptFactModel, ValueFactModel, PropertyFactModel, RelationFactModel]
DirectiveModel = Union[CreateAccountDirectiveModel, CreateConceptDirectiveModel, CreatePlatformDirectiveModel]


class DocumentMetadataModel(MetadataModel):
    title: Optional[str]
    file_name: Optional[str]
    file_type: Optional[str]
    size: Optional[int]
    created_time: Optional[int]
    access_time: Optional[int]
    modified_time: Optional[int]
    publication_date: Optional[int]
    publication_author: Optional[str]
    description: Optional[str]
    language: Optional[str]
    parent_uuid: Optional[str]
    url: Optional[str]
    platform: Optional[str]
    account: Optional[Tuple[str, ...]]
    access_level: Optional[str]
    user: Optional[str]
    path: Optional[str]
    trust_level: Optional[float]
    markers: Optional[Tuple[str, ...]]
    related_concept_id: Optional[str]
    preview_text: Optional[str]
    story: Optional[str]

    class Config:
        extra = 'allow'  # any other extra fields will be kept


class TalismanDocumentModel(BaseModel):
    id: str
    content: TreeDocumentContentModel
    metadata: Optional[DocumentMetadataModel]
    facts: Optional[Tuple[FactModel, ...]]  # pydantic fails to serialize FrozenSet[FactModel]
    directives: Optional[Tuple[DirectiveModel, ...]]

    def to_doc(self) -> TalismanDocument:
        type2fact_factory = defaultdict(list)
        for t, ff in map(lambda model: model.to_fact_factory(), (self.facts or tuple())):
            type2fact_factory[t].append(ff)

        def build_facts(fact_type: FactType, ids_mapping: Dict[str, AbstractFact]) -> Dict[str, AbstractFact]:
            return {fact.id: fact for fact in map(lambda factory: factory(ids_mapping), type2fact_factory.get(fact_type, []))}
        ids2facts = {}
        for ft in [FactType.CONCEPT, FactType.VALUE, FactType.RELATION, FactType.PROPERTY]:
            ids2facts.update(build_facts(ft, ids2facts))

        return TalismanDocument(
            doc_id=self.id, content=self.content.to_content(),
            metadata=self.metadata.to_metadata() if self.metadata is not None else None,
            facts=tuple(ids2facts.values()),
            directives=tuple(directive.to_directive() for directive in self.directives) if self.directives else None
        )

    @classmethod
    def build(cls, doc: AbstractTalismanDocument) -> 'TalismanDocumentModel':
        content_type = cls.__fields__['content'].type_
        return cls.construct(
            id=doc.doc_id,
            content=content_type.build(doc.content),
            metadata=DocumentMetadataModel(**doc.metadata) if doc.metadata is not None else None,
            facts=tuple(build_fact_model(fact, doc.content) for fact in doc.facts) if doc.facts is not None else None,
            directives=tuple(build_directive_model(directive) for directive in doc.directives) if doc.directives else None
        )
