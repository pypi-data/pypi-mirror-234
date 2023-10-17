from typing import TYPE_CHECKING, Optional

from LOGS.Entities.Datasets import Datasets
from LOGS.Entities.Documents import Documents
from LOGS.Entity.EntityRelation import EntityRelation
from LOGS.Entity.EntityRelations import EntityRelations

if TYPE_CHECKING:
    from LOGS.Entities.Dataset import Dataset
    from LOGS.Entities.Document import Document


class SampleRelations(EntityRelations):
    """Relations of a Sample with other entities"""

    _documents: Optional[EntityRelation["Document"]] = None
    _datasets: Optional[EntityRelation["Dataset"]] = None
    _labNotebookEntries: Optional[EntityRelation] = None

    @property
    def documents(self) -> Optional[EntityRelation["Document"]]:
        return self._documents

    @documents.setter
    def documents(self, value):
        self._documents = self._entityConverter(value, Documents)

    @property
    def datasets(self) -> Optional[EntityRelation["Dataset"]]:
        return self._datasets

    @datasets.setter
    def datasets(self, value):
        self._datasets = self._entityConverter(value, Datasets)

    @property
    def labNotebookEntries(self) -> Optional[EntityRelation]:
        return self._labNotebookEntries

    @labNotebookEntries.setter
    def labNotebookEntries(self, value):
        self._labNotebookEntries = self.checkAndConvertNullable(
            value, EntityRelation, "labNotebookEntries"
        )
