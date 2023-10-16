from typing import List, Optional

from LOGS.Auxiliary.Decorators import Endpoint
from LOGS.Entities.ProjectRelations import ProjectRelations
from LOGS.Entities.ProjectUserPermission import ProjectUserPermission
from LOGS.Entity.EntityWithIntId import EntityWithIntId
from LOGS.Interfaces.INamedEntity import INamedEntity
from LOGS.Interfaces.IOwnedEntity import IOwnedEntity
from LOGS.Interfaces.IUniqueEntity import IUniqueEntity
from LOGS.LOGSConnection import LOGSConnection


@Endpoint("projects")
class Project(INamedEntity, EntityWithIntId, IUniqueEntity, IOwnedEntity):
    _notes: Optional[str]
    _tags: Optional[List[str]]
    _relations: Optional[ProjectRelations]
    _userPermissions: Optional[List[ProjectUserPermission]]

    def __init__(
        self,
        ref=None,
        id: Optional[int] = None,
        connection: Optional[LOGSConnection] = None,
        name: Optional[str] = None,
    ):
        """Represents a connected LOGS entity type"""

        self._name = name
        self._notes = None
        self._tags = None
        self._relations = None
        self._userPermissions = None
        super().__init__(ref=ref, id=id, connection=connection)

    @property
    def notes(self) -> Optional[str]:
        return self._notes

    @notes.setter
    def notes(self, value):
        self._notes = self.checkAndConvertNullable(value, str, "notes")

    @property
    def tags(self) -> Optional[List[str]]:
        return self._tags

    @tags.setter
    def tags(self, value):
        self._tags = self.checkListAndConvertNullable(value, str, "tags")

    @property
    def relations(self) -> Optional[ProjectRelations]:
        return self._relations

    @relations.setter
    def relations(self, value):
        self._relations = self.checkAndConvertNullable(
            value, ProjectRelations, "relations"
        )

    @property
    def userPermissions(self) -> Optional[List[ProjectUserPermission]]:
        return self._userPermissions

    @userPermissions.setter
    def userPermissions(self, value):
        self._userPermissions = self.checkListAndConvertNullable(
            value, ProjectUserPermission, "userPermissions"
        )
