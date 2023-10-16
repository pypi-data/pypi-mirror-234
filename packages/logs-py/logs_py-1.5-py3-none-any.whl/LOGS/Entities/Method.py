from typing import Optional

from LOGS.Auxiliary.Decorators import Endpoint
from LOGS.Entity.EntityWithIntId import EntityWithIntId
from LOGS.Interfaces.INamedEntity import INamedEntity
from LOGS.Interfaces.IUniqueEntity import IUniqueEntity


@Endpoint("methods")
class Method(INamedEntity, EntityWithIntId, IUniqueEntity):
    _fullName: Optional[str] = None

    @property
    def fullName(self) -> Optional[str]:
        return self._fullName

    @fullName.setter
    def fullName(self, value):
        self._fullName = self.checkAndConvertNullable(value, str, "fullName")
