from datetime import datetime
from typing import TYPE_CHECKING, List, Optional

from LOGS.Auxiliary.Decorators import Endpoint
from LOGS.Auxiliary.MinimalModelGenerator import MinimalFromList
from LOGS.Entities.DocumentRelations import DocumentRelations
from LOGS.Entity.EntityMinimalWithIntId import EntityMinimalWithIntId
from LOGS.Entity.EntityWithIntId import EntityWithIntId
from LOGS.Entity.SerializeableContent import SerializeableContent
from LOGS.Interfaces.IOwnedEntity import IOwnedEntity
from LOGS.LOGSConnection import LOGSConnection

if TYPE_CHECKING:
    from LOGS.Entities.DatasetMinimal import DatasetMinimal
    from LOGS.Entities.PersonMinimal import PersonMinimal
    from LOGS.Entities.ProjectMinimal import ProjectMinimal
    from LOGS.Entities.SampleMinimal import SampleMinimal


class DocumentFile(SerializeableContent):
    _id: Optional[str] = None
    _name: Optional[str] = None
    _mime: Optional[str] = None
    _size: Optional[int] = None

    @property
    def id(self) -> Optional[str]:
        return self._id

    @id.setter
    def id(self, value):
        self._id = self.checkAndConvertNullable(value, str, "id")

    @property
    def name(self) -> Optional[str]:
        return self._name

    @name.setter
    def name(self, value):
        self._name = self.checkAndConvertNullable(value, str, "name")

    @property
    def mime(self) -> Optional[str]:
        return self._mime

    @mime.setter
    def mime(self, value):
        self._mime = self.checkAndConvertNullable(value, str, "mime")

    @property
    def size(self) -> Optional[int]:
        return self._size

    @size.setter
    def size(self, value):
        self._size = self.checkAndConvertNullable(value, int, "size")


@Endpoint("documents")
class Document(EntityWithIntId, IOwnedEntity):
    _name: Optional[str]
    _creationDate: Optional[datetime]
    _modificationDate: Optional[datetime]
    _notes: Optional[str]
    _publicationDate: Optional[datetime]
    _publicationType: Optional[EntityMinimalWithIntId]
    _doi: Optional[str]
    _url: Optional[str]
    _files: Optional[List[DocumentFile]]
    _authors: Optional[List["PersonMinimal"]]
    _projects: Optional[List["ProjectMinimal"]]
    _datasets: Optional[List["DatasetMinimal"]]
    _samples: Optional[List["SampleMinimal"]]
    _relations: Optional[DocumentRelations]

    def __init__(
        self,
        ref=None,
        id: Optional[int] = None,
        connection: Optional[LOGSConnection] = None,
    ):
        """Represents a connected LOGS entity type"""

        self._name = None
        self._creationDate = None
        self._modificationDate = None
        self._notes = None
        self._publicationDate = None
        self._publicationType = None
        self._doi = None
        self._url = None
        self._files = None
        self._authors = None
        self._projects = None
        self._datasets = None
        self._samples = None
        self._relations = None
        super().__init__(ref=ref, id=id, connection=connection)

    @property
    def name(self) -> Optional[str]:
        return self._name

    @name.setter
    def name(self, value):
        self._name = self.checkAndConvertNullable(value, str, "name")

    @property
    def creationDate(self) -> Optional[datetime]:
        return self._creationDate

    @creationDate.setter
    def creationDate(self, value):
        self._creationDate = self.checkAndConvertNullable(
            value, datetime, "creationDate"
        )

    @property
    def modificationDate(self) -> Optional[datetime]:
        return self._modificationDate

    @modificationDate.setter
    def modificationDate(self, value):
        self._modificationDate = self.checkAndConvertNullable(
            value, datetime, "modificationDate"
        )

    @property
    def notes(self) -> Optional[str]:
        return self._notes

    @notes.setter
    def notes(self, value):
        self._notes = self.checkAndConvertNullable(value, str, "notes")

    @property
    def publicationDate(self) -> Optional[datetime]:
        return self._publicationDate

    @publicationDate.setter
    def publicationDate(self, value):
        self._publicationDate = self.checkAndConvertNullable(
            value, datetime, "publicationDate"
        )

    @property
    def publicationType(self) -> Optional[EntityMinimalWithIntId]:
        return self._publicationType

    @publicationType.setter
    def publicationType(self, value):
        self._publicationType = self.checkAndConvertNullable(
            value, EntityMinimalWithIntId, "publicationType"
        )

    @property
    def doi(self) -> Optional[str]:
        return self._doi

    @doi.setter
    def doi(self, value):
        self._doi = self.checkAndConvertNullable(value, str, "doi")

    @property
    def url(self) -> Optional[str]:
        return self._url

    @url.setter
    def url(self, value):
        self._url = self.checkAndConvertNullable(value, str, "url")

    @property
    def files(self) -> Optional[List[DocumentFile]]:
        return self._files

    @files.setter
    def files(self, value):
        self._files = self.checkListAndConvertNullable(value, DocumentFile, "files")

    @property
    def authors(self) -> Optional[List["PersonMinimal"]]:
        return self._authors

    @authors.setter
    def authors(self, value):
        self._authors = MinimalFromList(
            value, "PersonMinimal", "authors", connection=self.connection
        )

    @property
    def projects(self) -> Optional[List["ProjectMinimal"]]:
        return self._projects

    @projects.setter
    def projects(self, value):
        self._projects = MinimalFromList(
            value, "ProjectMinimal", "projects", connection=self.connection
        )

    @property
    def datasets(self) -> Optional[List["DatasetMinimal"]]:
        return self._datasets

    @datasets.setter
    def datasets(self, value):
        self._datasets = MinimalFromList(
            value, "DatasetMinimal", "datasets", connection=self.connection
        )

    @property
    def samples(self) -> Optional[List["SampleMinimal"]]:
        return self._samples

    @samples.setter
    def samples(self, value):
        self._samples = MinimalFromList(
            value, "SampleMinimal", "samples", connection=self.connection
        )

    @property
    def relations(self) -> Optional[DocumentRelations]:
        return self._relations

    @relations.setter
    def relations(self, value):
        self._relations = self.checkAndConvertNullable(
            value, DocumentRelations, "relations"
        )
