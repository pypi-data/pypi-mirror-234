from typing import TYPE_CHECKING, Optional

from LOGS.Entity.EntityRelation import EntityRelation
from LOGS.Entity.EntityRelations import EntityRelations

if TYPE_CHECKING:
    from LOGS.Entities.Dataset import Dataset
    from LOGS.Entities.Document import Document


class DocumentRelations(EntityRelations):
    """Relations of a Document with other entities"""

    _documents: Optional[EntityRelation["Document"]] = None
    _datasets: Optional[EntityRelation["Dataset"]] = None

    @property
    def documents(self) -> Optional[EntityRelation["Document"]]:
        return self._documents

    @documents.setter
    def documents(self, value):
        from LOGS.Entities.Documents import Documents

        # print(">>>", value, self._entityConverter(value, Documents))
        self._documents = self._entityConverter(value, Documents)

    @property
    def datasets(self) -> Optional[EntityRelation["Dataset"]]:
        return self._datasets

    @datasets.setter
    def datasets(self, value):
        from LOGS.Entities.Datasets import Datasets

        self._datasets = self._entityConverter(value, Datasets)
