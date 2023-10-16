from typing import TYPE_CHECKING, Optional

from LOGS.Entities.Documents import Documents
from LOGS.Entity.EntityRelation import EntityRelation
from LOGS.Entity.EntityRelations import EntityRelations

if TYPE_CHECKING:
    from LOGS.Entities.Document import Document


class DatasetRelations(EntityRelations):
    """Relations of a Dataset with other entities"""

    _documents: Optional[EntityRelation["Document"]] = None
    _labNotebookEntries: Optional[EntityRelation] = None

    @property
    def documents(self) -> Optional[EntityRelation["Document"]]:
        return self._documents

    @documents.setter
    def documents(self, value):
        self._documents = self._entityConverter(value, Documents)

    @property
    def labNotebookEntries(self) -> Optional[EntityRelation]:
        return self._labNotebookEntries

    @labNotebookEntries.setter
    def labNotebookEntries(self, value):
        self._labNotebookEntries = self.checkAndConvertNullable(
            value, EntityRelation, "labNotebookEntries"
        )
