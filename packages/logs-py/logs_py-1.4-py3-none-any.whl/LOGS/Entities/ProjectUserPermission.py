from typing import TYPE_CHECKING, Optional

from LOGS.Auxiliary.MinimalModelGenerator import PersonMinimalFromDict
from LOGS.Entity.SerializeableContent import SerializeableContent

if TYPE_CHECKING:
    from LOGS.Entities.PersonMinimal import PersonMinimal


class ProjectUserPermission(SerializeableContent):
    _person: Optional["PersonMinimal"] = None
    _administer: Optional[bool] = None
    _add: Optional[bool] = None
    _read: Optional[bool] = None

    @property
    def person(self):
        return self._person

    @person.setter
    def person(self, value):
        self._person = PersonMinimalFromDict(value, "person")

    @property
    def administer(self) -> Optional[bool]:
        return self._administer

    @administer.setter
    def administer(self, value):
        self._administer = self.checkAndConvertNullable(value, bool, "administer")

    @property
    def add(self) -> Optional[bool]:
        return self._add

    @add.setter
    def add(self, value):
        self._add = self.checkAndConvertNullable(value, bool, "add")

    @property
    def read(self) -> Optional[bool]:
        return self._read

    @read.setter
    def read(self, value):
        self._read = self.checkAndConvertNullable(value, bool, "read")
