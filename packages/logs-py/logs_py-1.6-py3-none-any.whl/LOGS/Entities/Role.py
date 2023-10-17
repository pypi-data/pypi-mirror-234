from typing import TYPE_CHECKING, List, Optional

from LOGS.Auxiliary.Decorators import Endpoint
from LOGS.Auxiliary.MinimalModelGenerator import MinimalFromList
from LOGS.Entity.EntityWithIntId import EntityWithIntId
from LOGS.Interfaces.INamedEntity import INamedEntity
from LOGS.Interfaces.IUniqueEntity import IUniqueEntity

if TYPE_CHECKING:
    from LOGS.Entities.PersonMinimal import PersonMinimal


@Endpoint("roles")
class Role(INamedEntity, EntityWithIntId, IUniqueEntity):
    _description: Optional[str] = None
    _users: Optional[List["PersonMinimal"]]

    @property
    def description(self) -> Optional[str]:
        return self._description

    @description.setter
    def description(self, value):
        self._description = self.checkAndConvertNullable(value, str, "fullName")

    @property
    def users(self) -> Optional[List["PersonMinimal"]]:
        return self._users

    @users.setter
    def users(self, value):
        self._users = MinimalFromList(
            value, "PersonMinimal", "users", connection=self.connection
        )
