from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Literal, Optional, Sequence

from LOGS.Auxiliary.Constants import Constants
from LOGS.Entity.EntityRequestParameter import EntityRequestParameter
from LOGS.Interfaces.ICustomFields import ICustomFieldsRequest
from LOGS.Interfaces.IOwnedEntity import IOwnedEntityRequest
from LOGS.Interfaces.IUniqueEntity import IUniqueEntityRequest

ParsingStates = Literal[
    "ParsedSuccessfully", "NotParseable", "ParsingFailed", "NotYetParsed"
]


class DatasetOrder(Enum):
    ID_ASC = "ID_ASC"
    ID_DESC = "ID_DESC"
    NAME_ASC = "NAME_ASC"
    NAME_DESC = "NAME_DESC"
    ACQUISITION_DATE_ASC = "ACQUISITION_DATE_ASC"
    ACQUISITION_DATE_DESC = "ACQUISITION_DATE_DESC"
    METHOD_ASC = "METHOD_ASC"
    METHOD_DESC = "METHOD_DESC"
    EXPERIMENT_ASC = "EXPERIMENT_ASC"
    EXPERIMENT_DESC = "EXPERIMENT_DESC"
    DATE_ADDED_ASC = "DATE_ADDED_ASC"
    DATE_ADDED_DESC = "DATE_ADDED_DESC"
    INSTRUMENT_ASC = "INSTRUMENT_ASC"
    INSTRUMENT_DESC = "INSTRUMENT_DESC"
    SAMPLE_ASC = "SAMPLE_ASC"
    SAMPLE_DESC = "SAMPLE_DESC"
    FACILITY_ASC = "FACILITY_ASC"
    FACILITY_DESC = "FACILITY_DESC"
    PARSING_STATE_ASC = "PARSING_STATE_ASC"
    PARSING_STATE_DESC = "PARSING_STATE_DESC"
    PARSERID_ASC = "PARSERID_ASC"
    PARSERID_DESC = "PARSERID_DESC"
    DATASET_TYPE_ASC = "DATASET_TYPE_ASC"
    DATASET_TYPE_DESC = "DATASET_TYPE_DESC"


@dataclass
class DatasetRequestParameter(
    EntityRequestParameter,
    IUniqueEntityRequest,
    IOwnedEntityRequest,
    ICustomFieldsRequest,
):
    includeParameters: Optional[bool] = None
    methodIds: Optional[List[int]] = None
    formatIds: Optional[List[str]] = None
    experimentIds: Optional[List[int]] = None
    sampleIds: Optional[List[int]] = None
    acquisitionDateFrom: Optional[datetime] = None
    acquisitionDateTo: Optional[datetime] = None
    dateAddedFrom: Optional[datetime] = None
    dateAddedTo: Optional[datetime] = None
    operatorIds: Optional[List[int]] = None
    instrumentIds: Optional[List[int]] = None
    hasExperiment: Optional[bool] = None
    hasOperator: Optional[bool] = None
    documentIds: Optional[List[int]] = None
    equipmentIds: Optional[List[int]] = None
    projectIds: Optional[List[int]] = None
    organizationIds: Optional[List[int]] = None
    autoloadServerIds: Optional[List[int]] = None
    participatedPersonIds: Optional[List[int]] = None
    pathContains: Optional[str] = None
    parsingState: Optional[List[ParsingStates]] = None
    autoloadSourceId: Optional[int] = None
    orderBy: Optional[DatasetOrder] = None
    typeIds: Optional[List[str]] = None
    hashes: Optional[List[str]] = None
    includeSoftDeleted: Optional[Optional[bool]] = None
    isSoftDeleted: Optional[Optional[bool]] = None
    includeParsingInfo: Optional[bool] = None
    isClaimed: Optional[Optional[bool]] = None
    includeUnclaimed: Optional[Optional[bool]] = None
    files: Optional[Sequence[Constants.FILE_TYPE]] = None
    parameters: Optional[Dict[str, Any]] = None
