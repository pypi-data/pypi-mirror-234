from typing import List, Optional

from LOGS.Auxiliary.Decorators import Endpoint
from LOGS.Entity.EntityWithStrId import EntityWithStrId
from LOGS.Interfaces.INamedEntity import INamedEntity


@Endpoint("formats")
class FormatFormat(INamedEntity, EntityWithStrId):
    _description: Optional[str]
    _version: Optional[List[str]]

    @property
    def description(self) -> Optional[str]:
        return self._description

    @description.setter
    def description(self, value):
        self._description = self.checkAndConvertNullable(value, str, "description")

    @property
    def version(self) -> Optional[List[str]]:
        return self._version

    @version.setter
    def version(self, value):
        self._version = self.checkListAndConvertNullable(value, str, "version")
