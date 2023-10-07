from typing import Dict

from typing_extensions import Literal

from tdm.abstract.datamodel import AbstractFact, FactType
from tdm.datamodel.fact import PropertyFact, PropertyLinkValue
from tdm.json_schema.fact.common import AbstractFactModel, FactFactory, PropertyLinkValueModel


class PropertyFactModel(AbstractFactModel):
    fact_type: Literal[FactType.PROPERTY] = FactType.PROPERTY
    value: PropertyLinkValueModel

    def to_value(self, mapping: Dict[str, AbstractFact]) -> PropertyLinkValue:
        return PropertyLinkValue(
            property_id=self.value.property_id,
            from_fact=mapping[self.value.from_fact],
            to_fact=mapping[self.value.to_fact]
        )

    @property
    def fact_factory(self) -> FactFactory:
        return PropertyFact

    @classmethod
    def build_value(cls, value: PropertyLinkValue) -> PropertyLinkValueModel:
        return PropertyLinkValueModel.construct(property_id=value.property_id, from_fact=value.from_fact.id, to_fact=value.to_fact.id)
