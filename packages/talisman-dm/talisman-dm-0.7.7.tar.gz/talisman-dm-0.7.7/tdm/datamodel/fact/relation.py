from typing import Iterable, Optional, Tuple, Union

from tdm.abstract.datamodel import AbstractFact, AbstractTalismanSpan, FactMetadata, FactStatus, FactType
from tdm.abstract.datamodel.fact import AbstractLinkValue
from tdm.datamodel.fact import ACCOUNT_CONCEPT, PLATFORM_CONCEPT
from tdm.datamodel.fact.concept import ConceptFact

ACCOUNT_PLATFORM = "account_platform"


class RelationLinkValue(AbstractLinkValue[ConceptFact, ConceptFact]):
    @classmethod
    def validate_slots(cls, source: ConceptFact, target: ConceptFact):
        if source.fact_type is not FactType.CONCEPT:
            raise ValueError(f"inconsistent relation link source type: {source.fact_type}")
        if target.fact_type is not FactType.CONCEPT:
            raise ValueError(f"inconsistent relation link target type: {target.fact_type}")


class RelationFact(AbstractFact[RelationLinkValue]):
    def __init__(self, id_: Optional[str], status: FactStatus, type_id: str, value: RelationLinkValue,
                 mention: Iterable[AbstractTalismanSpan] = None, metadata: Optional[FactMetadata] = None):
        if not isinstance(value, RelationLinkValue):
            raise ValueError(f"illegal value type for relation fact: {type(value)}")
        if type_id == ACCOUNT_PLATFORM and (value.from_fact.type_id != ACCOUNT_CONCEPT or value.to_fact.type_id != PLATFORM_CONCEPT):
            raise ValueError(f"illegal relation {type_id} from {value.from_fact.type_id} to {value.to_fact.type_id}")
        super().__init__(id_, FactType.RELATION, status, type_id, value, mention, metadata)

    @AbstractFact.update_metadata
    def with_changes(self: 'RelationFact', *, status: FactStatus = None, type_id: str = None, value: RelationLinkValue = None,
                     mention: Tuple[AbstractTalismanSpan, ...] = None,
                     metadata: FactMetadata = None,
                     # metadata fields
                     fact_confidence: float = None,
                     value_confidence: Union[float, Tuple[float, ...]] = None) -> 'RelationFact':
        return RelationFact(
            self._id,
            status if status is not None else self._status,
            type_id if type_id is not None else self._type_id,
            value if value is not None else self._value,
            mention if mention is not None else self._mention,
            metadata if metadata is not None else self._metadata
        )
