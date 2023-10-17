from dataclasses import dataclass
from typing import Callable, Set, Type, TypeVar

from tdm.abstract.datamodel.identifiable import EnsureIdentifiable


_T = TypeVar('_T', bound='AbstractDomainType')


@dataclass(frozen=True)
class AbstractDomainType(EnsureIdentifiable):
    """
    Base class for knowledge base domain types

    Attributes
    --------
    name:
        The name of the domain type.
    """
    name: str

    @classmethod
    def constant_fields(cls) -> Set[str]:
        return set()

    @classmethod
    def name_filter(cls: Type[_T], name: str) -> Callable[[_T], bool]:
        def _filter(t: _T) -> bool:
            return t.name == name

        return _filter
