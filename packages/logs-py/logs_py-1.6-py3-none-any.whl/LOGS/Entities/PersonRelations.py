from typing import TYPE_CHECKING, Optional

from LOGS.Entities.Datasets import Datasets
from LOGS.Entities.Documents import Documents
from LOGS.Entity.EntityRelation import EntityRelation
from LOGS.Entity.EntityRelations import EntityRelations

if TYPE_CHECKING:
    from LOGS.Entities.Dataset import Dataset
    from LOGS.Entities.Document import Document
    from LOGS.Entities.Sample import Sample


class PersonRelations(EntityRelations):
    """Relations of a Person with other entities"""

    _documents: Optional[EntityRelation["Document"]] = None
    _datasets: Optional[EntityRelation["Dataset"]] = None
    _samples: Optional[EntityRelation["Sample"]] = None

    @property
    def documents(self) -> Optional[EntityRelation["Document"]]:
        return self._documents

    @documents.setter
    def documents(self, value):
        self._documents = self._entityConverter(value, Documents)

    @property
    def samples(self) -> Optional[EntityRelation["Sample"]]:
        return self._samples

    @samples.setter
    def samples(self, value):
        from LOGS.Entities.Samples import Samples

        self._samples = self._entityConverter(value, Samples)

    @property
    def datasets(self) -> Optional[EntityRelation["Dataset"]]:
        return self._datasets

    @datasets.setter
    def datasets(self, value):
        self._datasets = self._entityConverter(value, Datasets)
