from typing import Optional

from LOGS.Auxiliary.Decorators import Endpoint
from LOGS.Auxiliary.MinimalModelGenerator import MethodMinimalFromDict
from LOGS.Entities.MethodMinimal import MethodMinimal
from LOGS.Entity.EntityWithIntId import EntityWithIntId
from LOGS.Interfaces.ICreationRecord import ICreationRecord
from LOGS.Interfaces.IModificationRecord import IModificationRecord
from LOGS.Interfaces.INamedEntity import INamedEntity
from LOGS.Interfaces.IOwnedEntity import IOwnedEntity
from LOGS.Interfaces.IUniqueEntity import IUniqueEntity
from LOGS.LOGSConnection import LOGSConnection


@Endpoint("experiments")
class Experiment(
    INamedEntity,
    EntityWithIntId,
    IUniqueEntity,
    IOwnedEntity,
    IModificationRecord,
    ICreationRecord,
):
    _method: Optional[MethodMinimal]
    _notes: Optional[str]

    def __init__(
        self,
        ref=None,
        id: Optional[int] = None,
        connection: Optional[LOGSConnection] = None,
    ):
        """Represents a connected LOGS entity type"""

        self._method = None
        self._notes = None
        self._date_added = None
        self._date_last_modified = None

        super().__init__(ref=ref, id=id, connection=connection)

    def toDict(self):
        d = super().toDict()

        if self.method:
            d["measurementMethodId"] = self.method.id

        return d

    @property
    def method(self) -> Optional[MethodMinimal]:
        return self._method

    @method.setter
    def method(self, value):
        self._method = MethodMinimalFromDict(
            value, "method", connection=self.connection
        )

    @property
    def notes(self) -> Optional[str]:
        return self._notes

    @notes.setter
    def notes(self, value):
        self._notes = self.checkAndConvertNullable(value, str, "notes")

    @property
    def date_added(self) -> Optional[str]:
        return self._date_added

    @date_added.setter
    def date_added(self, value):
        self._date_added = self.checkAndConvertNullable(value, str, "date_added")

    @property
    def date_last_modified(self) -> Optional[str]:
        return self._date_last_modified

    @date_last_modified.setter
    def date_last_modified(self, value):
        self._date_last_modified = self.checkAndConvertNullable(
            value, str, "date_last_modified"
        )
