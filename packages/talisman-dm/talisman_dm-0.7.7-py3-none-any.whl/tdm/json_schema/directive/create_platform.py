from typing_extensions import Literal

from tdm.abstract.datamodel.directive import DirectiveType
from tdm.datamodel.directive import CreatePlatformDirective
from tdm.json_schema.directive.abstract import AbstractDirectiveModel


class CreatePlatformDirectiveModel(AbstractDirectiveModel):
    key: str
    platform_type: str
    name: str
    url: str

    directive_type: Literal[DirectiveType.CREATE_PLATFORM] = DirectiveType.CREATE_PLATFORM

    @classmethod
    def build(cls, directive: CreatePlatformDirective) -> 'CreatePlatformDirectiveModel':
        return cls.construct(
            key=directive.key,
            name=directive.name,
            url=directive.url,
            platform_type=directive.platform_type
        )

    def to_directive(self) -> CreatePlatformDirective:
        return CreatePlatformDirective(
            key=self.key,
            name=self.name,
            url=self.url,
            platform_type=self.platform_type
        )

    def __hash__(self):
        return hash((self.directive_type, self.key))
