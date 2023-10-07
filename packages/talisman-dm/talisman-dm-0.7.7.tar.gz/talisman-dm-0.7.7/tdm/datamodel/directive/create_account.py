from tdm.abstract.datamodel import AbstractDirective
from tdm.abstract.datamodel.directive import DirectiveType


class CreateAccountDirective(AbstractDirective):
    __slots__ = ('_key', '_platform_key', '_name', '_url')

    def __init__(self, key: str, platform_key: str, name: str, url: str):
        super().__init__(DirectiveType.CREATE_ACCOUNT)
        self._key = key
        self._platform_key = platform_key
        self._name = name
        self._url = url

    @property
    def key(self) -> str:
        return self._key

    @property
    def platform_key(self) -> str:
        return self._platform_key

    @property
    def name(self) -> str:
        return self._name

    @property
    def url(self) -> str:
        return self._url

    def __eq__(self, other):
        if not isinstance(other, AbstractDirective):
            return NotImplemented
        return isinstance(other, CreateAccountDirective) and other._key == self._key and other._platform_key == self._platform_key and \
            other._name == self._name and other._url == self._url

    def __hash__(self):
        return hash((super().__hash__(), self._key))
