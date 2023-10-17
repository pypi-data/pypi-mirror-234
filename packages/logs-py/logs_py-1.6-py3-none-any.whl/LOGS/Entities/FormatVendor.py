from typing import Optional

from LOGS.Auxiliary.Decorators import Endpoint
from LOGS.Entity.EntityWithStrId import EntityWithStrId
from LOGS.Interfaces.INamedEntity import INamedEntity


@Endpoint("vendors")
class FormatVendor(INamedEntity, EntityWithStrId):
    _description: Optional[str]
    _icon: Optional[str]

    @property
    def description(self) -> Optional[str]:
        return self._description

    @description.setter
    def description(self, value):
        self._description = self.checkAndConvertNullable(value, str, "description")

    @property
    def icon(self) -> Optional[str]:
        return self._icon

    @icon.setter
    def icon(self, value):
        self._icon = self.checkAndConvertNullable(value, str, "icon")
