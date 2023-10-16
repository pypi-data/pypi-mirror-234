from datetime import datetime
from typing import TYPE_CHECKING, Dict, List, Optional, Union, cast

from LOGS.Auxiliary.Decorators import Endpoint
from LOGS.Auxiliary.MinimalModelGenerator import (
    MinimalFromList,
    SampleTypeMinimalFromDict,
)
from LOGS.Entities.SampleRelations import SampleRelations
from LOGS.Entities.SampleTypeMinimal import SampleTypeMinimal
from LOGS.Entity.EntityWithIntId import EntityWithIntId
from LOGS.Interfaces.ICustomFields import ICustomFields
from LOGS.Interfaces.INamedEntity import INamedEntity
from LOGS.Interfaces.IOwnedEntity import IOwnedEntity
from LOGS.Interfaces.ISoftDeletable import ISoftDeletable
from LOGS.Interfaces.IUniqueEntity import IUniqueEntity
from LOGS.LOGSConnection import LOGSConnection

if TYPE_CHECKING:
    from LOGS.Entities.PersonMinimal import PersonMinimal
    from LOGS.Entities.Project import Project
    from LOGS.Entities.ProjectMinimal import ProjectMinimal


@Endpoint("samples")
class Sample(
    INamedEntity,
    EntityWithIntId,
    IUniqueEntity,
    IOwnedEntity,
    ICustomFields,
    ISoftDeletable,
):
    _type: Optional[SampleTypeMinimal]
    _fullName: Optional[str] = None
    _createdAt: Optional[datetime]
    _preparedAt: Optional[datetime]
    _discardedAt: Optional[datetime]
    _projects: Optional[List["ProjectMinimal"]]
    _preparedBy: Optional[List["PersonMinimal"]]
    _discardedBy: Optional[List["PersonMinimal"]]
    _other: Optional[str]
    _notes: Optional[str]
    _relations: Optional[SampleRelations]
    _tags: Optional[Dict[str, Union[str, int, float]]]

    def __init__(
        self,
        ref=None,
        id: Optional[int] = None,
        connection: Optional[LOGSConnection] = None,
        name: str = "",
        preparedAt: Optional[datetime] = None,
        preparedBy: Optional[List["PersonMinimal"]] = None,
        projects: Optional[List[Union["ProjectMinimal", "Project"]]] = None,
    ):
        self._name = name
        self._fullName = name
        self._preparedAt = preparedAt
        self._preparedBy = preparedBy
        self._projects = cast(Optional[List["ProjectMinimal"]], projects)
        self._type = None
        self._createdAt = None
        self._discardedAt = None
        self._discardedBy = None
        self._other = None
        self._notes = None
        self._customFields = None
        self._relations = None
        self._tags = None

        if ref != None and isinstance(ref, (str, int, float)):
            ref = {"text": str(ref)}

        super().__init__(connection=connection, id=id, ref=ref)

    @property
    def type(self) -> Optional[SampleTypeMinimal]:
        return self._type

    @type.setter
    def type(self, value):
        self._type = SampleTypeMinimalFromDict(
            value, "type", connection=self.connection
        )

    @property
    def fullName(self) -> Optional[str]:
        return self._fullName

    @fullName.setter
    def fullName(self, value):
        self._fullName = self.checkAndConvertNullable(value, str, "fullName")

    @property
    def createdAt(self) -> Optional[datetime]:
        return self._createdAt

    @createdAt.setter
    def createdAt(self, value):
        self._createdAt = self.checkAndConvertNullable(value, datetime, "createdAt")

    @property
    def preparedAt(self) -> Optional[datetime]:
        return self._preparedAt

    @preparedAt.setter
    def preparedAt(self, value):
        self._preparedAt = self.checkAndConvert(value, datetime, "preparedAt")

    @property
    def discardedAt(self) -> Optional[datetime]:
        return self._discardedAt

    @discardedAt.setter
    def discardedAt(self, value):
        self._discardedAt = self.checkAndConvertNullable(value, datetime, "discardedAt")

    # @property
    # def discarded(self) -> Optional[bool]:
    #     return self._discarded

    # @discarded.setter
    # def discarded(self, value):
    #     self._discarded = self.checkAndConvertNullable(value, bool, "discarded")

    @property
    def other(self) -> Optional[str]:
        return self._other

    @other.setter
    def other(self, value):
        self._other = self.checkAndConvertNullable(value, str, "other")

    # @property
    # def preparators(self) -> List[Person]:
    #     return self._preparators

    # @preparators.setter
    # def preparators(self, value):
    #     self._preparators = self.checkAndConvertNullable(value, List, "preparators")

    # @property
    # def discarders(self) -> List[Person]:
    #     return self._discarders

    # @discarders.setter
    # def discarders(self, value):
    #     self._discarders = self.checkAndConvertNullable(value, List, "discarders")

    @property
    def projects(self) -> Optional[List["ProjectMinimal"]]:
        return self._projects

    @projects.setter
    def projects(self, value):
        self._projects = MinimalFromList(
            value, "ProjectMinimal", "projects", connection=self.connection
        )

    # @property
    # def documents(self) -> List[Document]:
    #     return self._documents

    # @documents.setter
    # def documents(self, value):
    #     self._documents = self.checkAndConvertNullable(value, List, "documents")

    @property
    def preparedBy(self) -> Optional[List["PersonMinimal"]]:
        return self._preparedBy

    @preparedBy.setter
    def preparedBy(self, value):
        self._preparedBy = MinimalFromList(
            value, "PersonMinimal", "preparedBy", connection=self.connection
        )

    @property
    def discardedBy(self) -> Optional[List["PersonMinimal"]]:
        return self._discardedBy

    @discardedBy.setter
    def discardedBy(self, value):
        self._discardedBy = MinimalFromList(
            value, "PersonMinimal", "discardedBy", connection=self.connection
        )

    @property
    def notes(self) -> Optional[str]:
        return self._notes

    @notes.setter
    def notes(self, value):
        self._notes = self.checkAndConvertNullable(value, str, "notes")

    @property
    def relations(self) -> Optional[SampleRelations]:
        return self._relations

    @relations.setter
    def relations(self, value):
        self._relations = self.checkAndConvertNullable(
            value, SampleRelations, "relations"
        )

    @property
    def tags(self) -> Optional[Dict[str, Union[str, int, float]]]:
        return self._tags

    @tags.setter
    def tags(self, value):
        self._tags = self.checkAndConvertNullable(value, dict, "tags")
        self._tags = {
            str(k): v
            for k, v in self._tags.items()
            if v is not None and k != "Name" and isinstance(v, (str, int, float))
        }

        if not self._tags:
            self._tags = None
