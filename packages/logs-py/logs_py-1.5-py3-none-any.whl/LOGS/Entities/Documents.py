from LOGS.Auxiliary.Decorators import Endpoint
from LOGS.Entities.Document import Document
from LOGS.Entities.DocumentRequestParameter import DocumentRequestParameter
from LOGS.Entity.EntityIterator import EntityIterator


@Endpoint("documents")
class Documents(EntityIterator[Document, DocumentRequestParameter]):
    """LOGS connected Document iterator"""

    _generatorType = Document
    _parameterType = DocumentRequestParameter
