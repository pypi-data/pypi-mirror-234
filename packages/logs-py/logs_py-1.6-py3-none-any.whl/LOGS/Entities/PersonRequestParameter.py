from dataclasses import dataclass
from typing import List, Optional

from LOGS.Entity.EntityRequestParameter import EntityRequestParameter


@dataclass
class PersonRequestParameter(EntityRequestParameter):
    categoryId: Optional[int] = None
    organizationId: Optional[int] = None
    login: Optional[str] = None
    firstName: Optional[str] = None
    lastName: Optional[str] = None
    documentIds: Optional[List[int]] = None
    projectIds: Optional[List[int]] = None
    datasetIds: Optional[List[int]] = None
    sampleIds: Optional[List[int]] = None
    organizationIds: Optional[List[int]] = None
