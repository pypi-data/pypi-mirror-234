from tdm.abstract.datamodel import AbstractDirective
from tdm.abstract.datamodel.directive import DirectiveType


class CreatePlatformDirective(AbstractDirective):
    __slots__ = ('_key', '_name', '_platform_type', '_url')

    def __init__(self, key: str, name: str, platform_type: str, url: str):
        super().__init__(DirectiveType.CREATE_PLATFORM)
        self._key = key
        self._name = name
        self._url = url
        self._platform_type = platform_type

    @property
    def key(self) -> str:
        return self._key

    @property
    def platform_type(self) -> str:
        return self._platform_type

    @property
    def name(self) -> str:
        return self._name

    @property
    def url(self) -> str:
        return self._url

    def __eq__(self, other):
        if not isinstance(other, AbstractDirective):
            return NotImplemented
        return isinstance(other, CreatePlatformDirective) and other._key == self._key and other._name == self._name and \
            other._platform_type == self._platform_type and other._url == self._url

    def __hash__(self):
        return hash((super().__hash__(), self._key))
