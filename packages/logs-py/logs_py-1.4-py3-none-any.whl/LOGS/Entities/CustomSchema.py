from datetime import datetime
from typing import TYPE_CHECKING, Optional

from LOGS.Entity.EntityWithStrId import EntityWithStrId
from LOGS.Interfaces.INamedEntity import INamedEntity
from LOGS.Interfaces.IOwnedEntity import IOwnedEntity
from LOGS.LOGSConnection import LOGSConnection

if TYPE_CHECKING:
    pass


class CustomSchema(EntityWithStrId, IOwnedEntity, INamedEntity):
    _createdAt: Optional[datetime]
    _enabled: Optional[bool]

    def __init__(
        self,
        ref=None,
        id: Optional[str] = None,
        connection: Optional[LOGSConnection] = None,
    ):
        self._name = None
        self._createdAt = None
        self._enabled = None
        super().__init__(ref=ref, id=id, connection=connection)

    @property
    def createdAt(self) -> Optional[datetime]:
        return self._createdAt

    @createdAt.setter
    def createdAt(self, value):
        self._createdAt = self.checkAndConvertNullable(value, datetime, "createdAt")

    @property
    def enabled(self) -> Optional[bool]:
        return self._enabled

    @enabled.setter
    def enabled(self, value):
        self._enabled = self.checkAndConvertNullable(value, bool, "enabled")
