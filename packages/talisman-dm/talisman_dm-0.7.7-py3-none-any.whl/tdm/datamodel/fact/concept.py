import logging
from typing import Iterable, Optional, Tuple, Union

from tdm.abstract.datamodel import AbstractFact, AbstractTalismanSpan, FactMetadata, FactStatus, FactType

ConceptValueType = str  # TODO: describe concept type

UNKNOWN_TYPE_ID = "-1"
PLATFORM_CONCEPT = "platform"
ACCOUNT_CONCEPT = "account"

logger = logging.getLogger(__name__)


class ConceptFact(AbstractFact[ConceptValueType]):
    def __init__(self, id_: Optional[str], status: FactStatus, type_id: str,
                 value: Union[ConceptValueType, Iterable[ConceptValueType]] = tuple(),
                 mention: Optional[Iterable[AbstractTalismanSpan]] = None,
                 metadata: Optional[FactMetadata] = None):
        if value is None:
            value = tuple()
            logger.warning("value must not be None, value=tuple()")
        elif isinstance(value, ConceptValueType):
            pass  # do nothing
        elif isinstance(value, Iterable) and all(isinstance(v, ConceptValueType) for v in value):
            value = tuple(value)
        else:
            raise ValueError(f"Bad concept fact value {value}")
        if type_id == UNKNOWN_TYPE_ID and (status is not FactStatus.AUTO or not isinstance(value, ConceptValueType)):
            raise ValueError("unknown type id could be used only for auto facts with single value")
        super().__init__(id_, FactType.CONCEPT, status, type_id, value, mention, metadata)

    @AbstractFact.update_metadata
    def with_changes(self: 'ConceptFact', *, status: FactStatus = None, type_id: str = None,
                     value: Union[ConceptValueType, Tuple[ConceptValueType, ...]] = None,
                     mention: Tuple[AbstractTalismanSpan, ...] = None,
                     metadata: FactMetadata = None,
                     value_confidence: Union[float, Tuple[float, ...]] = None) -> 'ConceptFact':
        return ConceptFact(
            self._id,
            status if status is not None else self._status,
            type_id if type_id is not None else self._type_id,
            value if value is not None else self._value,
            mention if mention is not None else self._mention,
            metadata if metadata is not None else self._metadata
        )
