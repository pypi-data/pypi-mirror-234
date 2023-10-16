from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import List, Optional

from LOGS.Entity.EntityRequestParameter import EntityRequestParameter
from LOGS.Interfaces.ICustomFields import ICustomFieldsRequest
from LOGS.Interfaces.INamedEntity import INamedEntityRequest
from LOGS.Interfaces.IOwnedEntity import IOwnedEntityRequest
from LOGS.Interfaces.IPaginationRequest import IPaginationRequest
from LOGS.Interfaces.ISoftDeletable import ISoftDeletableRequest


class SampleOrder(Enum):
    ID_ASC = "ID_ASC"
    ID_DESC = "ID_DESC"
    CREATION_DATE_ASC = "CREATION_DATE_ASC"
    CREATION_DATE_DESC = "CREATION_DATE_DESC"
    PREPARATION_DATE_ASC = "PREPARATION_DATE_ASC"
    PREPARATION_DATE_DESC = "PREPARATION_DATE_DESC"
    NAME_ASC = "NAME_ASC"
    NAME_DESC = "NAME_DESC"
    SAMPLE_TYPE_ASC = "SAMPLE_TYPE_ASC"
    SAMPLE_TYPE_DESC = "SAMPLE_TYPE_DESC"


@dataclass
class SampleRequestParameter(
    EntityRequestParameter,
    IPaginationRequest,
    IOwnedEntityRequest,
    ICustomFieldsRequest,
    INamedEntityRequest,
    ISoftDeletableRequest,
):
    includePermissions: Optional[bool] = None
    includeRelationLink: Optional[bool] = None
    includeRelationCount: Optional[bool] = None

    projectIds: Optional[List[int]] = None
    organizationIds: Optional[List[int]] = None
    preparedByIds: Optional[List[int]] = None
    documentIds: Optional[List[int]] = None
    discardedByIds: Optional[List[int]] = None
    participatedPersonIds: Optional[List[int]] = None
    typeIds: Optional[List[str]] = None
    excludeDiscarded: Optional[bool] = None
    preparedAtFrom: Optional[datetime] = None
    preparedAtTo: Optional[datetime] = None
    includeTags: Optional[bool] = None
    orderBy: Optional[SampleOrder] = None
