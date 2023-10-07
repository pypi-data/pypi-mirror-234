from typing_extensions import Literal

from tdm.abstract.datamodel.directive import DirectiveType
from tdm.datamodel.directive import CreateAccountDirective
from tdm.json_schema.directive.abstract import AbstractDirectiveModel


class CreateAccountDirectiveModel(AbstractDirectiveModel):
    key: str
    platform_key: str
    name: str
    url: str

    directive_type: Literal[DirectiveType.CREATE_ACCOUNT] = DirectiveType.CREATE_ACCOUNT

    @classmethod
    def build(cls, directive: CreateAccountDirective) -> 'CreateAccountDirectiveModel':
        return cls.construct(
            key=directive.key,
            platform_key=directive.platform_key,
            name=directive.name,
            url=directive.url
        )

    def to_directive(self) -> CreateAccountDirective:
        return CreateAccountDirective(
            key=self.key,
            platform_key=self.platform_key,
            name=self.name,
            url=self.url
        )

    def __hash__(self):
        return hash((self.directive_type, self.key))
