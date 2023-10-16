#!/usr/bin/env python3
"""
A library to access the LOGS API via Python
"""
# +---------------+-----------+--------------+-------------------------+
# |  When         |  Version  |  Who         |  What                   |
# +===============+===========+==============+=========================+
# |  2021-07-16   |   0.1     |  Sina Kazemi |  First version          |
# +---------------+-----------+--------------+-------------------------+
# |  2021-09-18   |   1.0     |  Sina Kazemi |  First official release |
# +---------------+-----------+--------------+-------------------------+

import json
import os
from typing import (
    Any,
    Dict,
    List,
    Optional,
    Sequence,
    Type,
    TypeVar,
    Union,
    cast,
    overload,
)
from uuid import UUID

from LOGS.Auxiliary import (
    Constants,
    EntityCreatingException,
    EntityDeletingException,
    EntityNotFoundException,
    EntityUpdatingException,
    LOGSException,
    Tools,
    formatErrorMessage,
)
from LOGS.Entities import (
    AutoloadSource,
    Dataset,
    DatasetCreator,
    DatasetMatching,
    DatasetRequestParameter,
    Datasets,
    DatasetsUpdatableFiles,
    Document,
    DocumentRequestParameter,
    Documents,
    Entities,
    EntitiesRequestParameter,
    EntityOriginWriteModelWithId,
    Equipment,
    Experiment,
    ExperimentRequestParameter,
    Experiments,
    FileEntry,
    Instrument,
    InstrumentRequestParameter,
    Instruments,
    IUniqueEntity,
    LabNotebookEntry,
    Method,
    MethodRequestParameter,
    Methods,
    Origin,
    OriginRequestParameter,
    Origins,
    Person,
    PersonRequestParameter,
    Persons,
    Project,
    ProjectRequestParameter,
    Projects,
    Sample,
    SampleRequestParameter,
    Samples,
)
from LOGS.Entities.AutoloadConfiguration import AutoloadConfiguration
from LOGS.Entities.AutoloadConfigurationRequestParameter import (
    AutoloadConfigurationRequestParameter,
)
from LOGS.Entities.AutoloadConfigurations import AutoloadConfigurations
from LOGS.Entities.AutoloadSourceRequestParameter import AutoloadSourceRequestParameter
from LOGS.Entities.AutoloadSources import AutoloadSources
from LOGS.Entities.Format import Format
from LOGS.Entities.FormatFormat import FormatFormat
from LOGS.Entities.FormatFormatRequestParameter import FormatFormatRequestParameter
from LOGS.Entities.FormatFormats import FormatFormats
from LOGS.Entities.FormatInstrument import FormatInstrument
from LOGS.Entities.FormatInstrumentRequestParameter import (
    FormatInstrumentRequestParameter,
)
from LOGS.Entities.FormatInstruments import FormatInstruments
from LOGS.Entities.FormatMethod import FormatMethod
from LOGS.Entities.FormatMethodRequestParameter import FormatMethodRequestParameter
from LOGS.Entities.FormatMethods import FormatMethods
from LOGS.Entities.FormatRequestParameter import FormatRequestParameter
from LOGS.Entities.Formats import Formats
from LOGS.Entities.FormatVendor import FormatVendor
from LOGS.Entities.FormatVendorRequestParameter import FormatVendorRequestParameter
from LOGS.Entities.FormatVendors import FormatVendors
from LOGS.Entities.LabNotebookEntries import LabNotebookEntries
from LOGS.Entities.LabNotebookEntryRequestParameter import (
    LabNotebookEntryRequestParameter,
)
from LOGS.Entities.Role import Role
from LOGS.Entities.RoleRequestParameter import RoleRequestParameter
from LOGS.Entities.Roles import Roles
from LOGS.Entity import Entity, EntityIterator, EntityWithIntId
from LOGS.LOGSConnection import LOGSConnection

_T = TypeVar(
    "_T",
    Document,
    Person,
    Project,
    Sample,
    Dataset,
    AutoloadSource,
    AutoloadConfiguration,
    Equipment,
    Experiment,
    Instrument,
    Method,
    LabNotebookEntry,
    EntityWithIntId,
    Origin,
    Format,
    Role,
    FormatVendor,
    FormatMethod,
    FormatInstrument,
    FormatFormat,
)


class LOGS:
    """Python class to access the LOGS web API"""

    _connection: LOGSConnection
    _entities: List[Type] = [
        Document,
        Person,
        Project,
        Sample,
        Dataset,
        AutoloadSource,
        AutoloadConfiguration,
        Equipment,
        Experiment,
        Instrument,
        Method,
        LabNotebookEntry,
        Origin,
    ]
    _entityByName = {t.__name__: t for t in _entities}
    _defaultConfigFile: str = "logs.json"
    _currentUser: Person

    def __init__(
        self,
        url: Optional[str] = None,
        apiKey: Optional[str] = None,
        configFile: Optional[str] = None,
        verbose: bool = False,
        verify: bool = True,
    ):
        """Checks the connection to the server on creation

        :param url: URL to specific LOGS group (e.g. https://mylogs/mygroup or https://mylogs:80/mygroup/api/0.1)
        :param api_key: The API key that grants access to LOGS (you need to generate on in LOGS and copy it)
        :param verbose: If set you see some information about the server connection. Defaults to False.

        :raises: Exception: URL does not defined or is invalid.
        :raises: Exception: The URL does not define a group.
        :raises: Exception: Server cannot be reached.
        """
        _url = url
        _apiKey = apiKey

        if not configFile and os.path.isfile(self._defaultConfigFile):
            configFile = self._defaultConfigFile

        if configFile:
            config = self._readConfig(configFile)
            if "url" in config:
                _url = config["url"]
            if "apiKey" in config:
                _apiKey = config["apiKey"]

        if url:
            _url = url

        if apiKey:
            _apiKey = apiKey

        if not _url:
            raise LOGSException("The url to the LOGS server must be provided.")

        if not _apiKey:
            raise LOGSException(
                "The API key to access the server %a must be provided" % _url
            )

        self.verbose = verbose
        self.promptPrefix = "LOGSAPI>"

        self._connection = LOGSConnection(
            url=_url, apiKey=_apiKey, verbose=verbose, verify=verify
        )

        self._currentUser = self._fetchCurrentUser()

    def _fetchCurrentUser(self) -> Person:
        data, errors = self._connection.getEndpoint(["session"])
        if errors:
            raise LOGSException(message=errors)

        if not isinstance(data, dict):
            raise LOGSException(
                "Unexpected respons from session endpoint. Could not get current user."
            )

        person = None
        if "person" in data:
            person = Person(data["person"])

        if not person or not person.id:
            raise LOGSException(
                "Unexpected respons from session endpoint. Could not get current user."
            )

        return person

    def _readConfig(self, path: str) -> dict:
        if not os.path.isfile(path):
            raise LOGSException("Could not find config file %a" % path)

        with open(path, "r") as f:
            try:
                config = json.load(f)
            except json.JSONDecodeError as e:
                raise LOGSException(
                    "Could not read config from file %a: %s" % (path, str(e))
                )
        return config

    @classmethod
    def getHumanReadableSize(cls, size: float, suffix="B"):
        for unit in Constants.byteUnits:
            if abs(size) < 1024.0:
                return "%3.1f%s%s" % (size, unit, suffix)
            size /= 1024.0
        return "%.1f%s%s" % (size, "Yi", suffix)

    def _fetchEntity(self, entityType: Type[_T], id: Union[int, str]) -> _T:
        e = entityType(id=cast(Any, id), connection=self._connection)
        e.fetch()
        return e

    def _updateEntitiesByTypeName(self, typeDict: Dict[str, Any]):
        for typeName, entities in typeDict.items():
            if not entities:
                continue
            t = self._entityByName.get(typeName, None)
            if not t:
                continue
            self._updateEntities(cast(Any, t), entities)

    def _updateEntities(self, entityType: Type, entities: List[Constants.ENTITIES]):
        if not entityType._endpoint:
            raise NotImplementedError(
                "Updating of entity type %a is not implemented."
                % (
                    type(self).__name__
                    if type(self).__name__ != Entity.__name__
                    else "unknown"
                )
            )

        if len(entities) < 1:
            return
        elif len(entities) == 1:
            if not entities[0].id:
                raise EntityNotFoundException(entities[0])

            data, errors = self._connection.putEndpoint(
                entityType._endpoint + [str(entities[0].id)], data=entities[0].toDict()
            )
            entities[0].override(data)
        else:
            data, errors = self._connection.postEndpoint(
                entityType._endpoint + ["bulk_edit"],
                data=[e.toDict() for e in entities],
            )
            if (
                isinstance(data, dict)
                and "results" in data
                and isinstance(data["results"], list)
            ):
                for i, d in enumerate(data["results"]):
                    entities[i].override(d)

        if errors:
            raise EntityUpdatingException(entity=entities, errors=errors)

    def _createDataset(self, dataset: Dataset):
        data = DatasetCreator(connection=self._connection, dataset=dataset).create()
        # TODO: The following is not optimal. DatasetCreator should directly set the dataset properties (add dataset write model to multipart)
        if (
            "results" in data
            and isinstance(data["results"], list)
            and len(data["results"]) == 1
        ):
            dataset.override(data["results"][0])
            dataset.connection = self._connection

    def _createEntitiesByTypeName(self, typeDict: Dict[str, Entity]):
        for typeName, entities in typeDict.items():
            if not entities:
                continue
            t = self._entityByName.get(typeName, None)

            if not t:
                continue

            self._createEntities(cast(Any, t), cast(Any, entities))

    def _addOriginToEntity(
        self, endpoint: List[str], entity: Optional[EntityOriginWriteModelWithId]
    ):
        return self._addOriginToEntities(endpoint, [entity])

    def _addOriginToEntities(
        self,
        endpoint: List[str],
        entities: List[Optional[EntityOriginWriteModelWithId]],
    ):
        entities = [e for e in entities if e]
        if len(entities) == 1:
            data, errors = self._connection.postEndpoint(
                endpoint + ["origin"], data=[e.toDict() for e in entities if e]
            )
            if errors:
                indent = " " * 2
                message = ""
                if isinstance(data, list):
                    message = "%sCould not add origin to %s %a" % (
                        "\n" + indent if errors and len(errors) > 1 else "",
                        Tools.plural("entity", entities),
                        Tools.eclipsesJoin(", ", [e.id for e in entities if e]),
                    )

                # indent *= 2
                if errors:
                    message += ": " + formatErrorMessage(errors=errors, indent=indent)

                raise LOGSException(message=message)

        # for o in entities:
        #     print(">>>>>", o.toDict())
        # data, errors = self._connection.postEndpoint(
        #     entityType._endpoint + ["bulk_create"],
        #     data=[e.toDict() for e in entities],
        # )

    def _createEntityOriginWriteModel(
        self, entity: Union[Entity, IUniqueEntity]
    ) -> Optional[EntityOriginWriteModelWithId]:
        if isinstance(entity, IUniqueEntity) and (
            entity._foreignUid or entity._foreignOrigin
        ):
            if isinstance(entity, Entity):
                model = EntityOriginWriteModelWithId(
                    id=entity.id, uid=entity._foreignUid, origin=entity._foreignOrigin
                )
                if model.uid:
                    setattr(entity, "uid", model.uid)
                if model.uid:
                    setattr(entity, "origin", model.origin)
                return model

        return None

    def _createEntities(self, entityType: Type[Entity], entities: List[Entity]):
        if not entityType._endpoint:
            raise NotImplementedError(
                "Creating of entity type %a is not implemented."
                % (
                    entityType.__name__
                    if entityType.__name__ != Entity.__name__
                    else "unknown"
                )
            )

        datasets = cast(List[Dataset], [e for e in entities if isinstance(e, Dataset)])
        entities = [e for e in entities if not isinstance(e, Dataset)]

        if len(datasets) > 0:
            for dataset in datasets:
                self._createDataset(dataset)
                self._addOriginToEntity(
                    entityType._endpoint, self._createEntityOriginWriteModel(dataset)
                )

        errors = None
        if len(entities) == 1:
            data, errors = self._connection.postEndpoint(
                entityType._endpoint, data=entities[0].toDict()
            )
            if errors:
                raise EntityCreatingException(entity=entities, errors=errors)

            entities[0].override(data)
            entities[0].connection = self._connection
            self._addOriginToEntity(
                entityType._endpoint, self._createEntityOriginWriteModel(entities[0])
            )

        elif len(entities) > 1:
            data, errors = self._connection.postEndpoint(
                entityType._endpoint + ["bulk_create"],
                data=[e.toDict() for e in entities],
            )
            if errors:
                raise EntityCreatingException(entity=entities, errors=errors)

            if (
                isinstance(data, dict)
                and "results" in data
                and isinstance(data["results"], list)
            ):
                for i, d in enumerate(data["results"]):
                    entities[i].override(d)
                    entities[i].connection = self._connection
                self._addOriginToEntities(
                    entityType._endpoint,
                    [self._createEntityOriginWriteModel(e) for e in entities],
                )

    def _deleteEntitiesByTypeName(
        self,
        typeDict: Dict[str, List[Union[Constants.ID_TYPE, None]]],
        permanently: bool = False,
    ):
        for typeName, entities in typeDict.items():
            if not entities:
                continue
            t = self._entityByName.get(typeName, None)
            if not t:
                continue
            self._deleteEntities(cast(Any, t), [e for e in entities if e], permanently)

    def _deleteEntities(
        self,
        entityType: Type,
        entityIds: List[Constants.ID_TYPE],
        permanently: bool = False,
    ):
        if not entityType._endpoint:
            raise NotImplementedError(
                "Deleting of entity type %a is not implemented."
                % (
                    type(self).__name__
                    if type(self).__name__ != Entity.__name__
                    else "unknown"
                )
            )

        if len(entityIds) < 1:
            return
        elif len(entityIds) == 1:
            _, errors = self._connection.deleteEndpoint(
                entityType._endpoint + [str(entityIds[0])],
                parameters={"deletePermanently": permanently} if permanently else {},
            )
        else:
            _, errors = self._connection.postEndpoint(
                entityType._endpoint + ["bulk_delete"],
                data=[id for id in entityIds],
                parameters={"deletePermanently": permanently} if permanently else {},
            )

        if errors:
            raise EntityDeletingException(entityIds=entityIds, errors=errors)

    @classmethod
    def _collectTypes(cls, entities: list) -> Dict[str, Any]:
        result: Dict[str, Any] = {k: [] for k in cls._entityByName.keys()}
        result["unknown"] = []

        for entity in entities:
            unknown = True

            for k, v in cls._entityByName.items():
                if isinstance(entity, v):
                    result[k].append(entity)
                    unknown = False
                    break

            if unknown:
                result["unknown"].append(entity)
        return result

    def printServerStatus(self):
        self._connection.printServerStatus()

    @overload
    def update(self, entities: Constants.ENTITIES):
        ...

    @overload
    def update(self, entities: List[Constants.ENTITIES]):
        ...

    # Implementation of overload
    def update(self, entities: Any):
        def decorator(entities: Any):
            types = self._collectTypes(entities)
            if len(types["unknown"]) > 0:
                raise EntityUpdatingException(
                    types["unknown"][0],
                    errors=[
                        "Entity type %a not valid for this action."
                        % type(types["unknown"][0]).__name__
                    ],
                )

            self._updateEntitiesByTypeName(types)

        if not isinstance(entities, list):
            entities = [entities]
        return decorator(entities)

    @overload
    def create(self, entities: _T):
        ...

    @overload
    def create(self, entities: List[_T]):
        ...

    # Implementation of overload
    def create(self, entities: Any):
        def decorator(entities: List[Entity]):
            types = self._collectTypes(entities)
            if len(types["unknown"]) > 0:
                raise EntityCreatingException(
                    types["unknown"][0],
                    errors=[
                        "Entity type %a not valid for this action"
                        % type(types["unknown"][0]).__name__
                    ],
                )

            self._createEntitiesByTypeName(types)

        if not isinstance(entities, list):
            entities = [entities]
        decorator(entities)

    @overload
    def delete(self, entities: Constants.ENTITIES, permanently=False):
        ...

    @overload
    def delete(self, entities: List[Constants.ENTITIES], permanently=False):
        ...

    # Implementation of overload
    def delete(self, entities: Any = None, permanently=False):
        def decorator(entities: Any):
            types: Dict[str, List[Union[Constants.ID_TYPE, None]]] = self._collectTypes(
                entities
            )
            types = {
                typeName: [cast(Entity, e).id for e in entities if e]
                for typeName, entities in types.items()
            }
            if len(types["unknown"]) > 0:
                raise EntityDeletingException(
                    types["unknown"][0],
                    errors=[
                        "Entity type %a not valid for this action"
                        % type(types["unknown"][0]).__name__
                    ],
                )

            self._deleteEntitiesByTypeName(types, permanently=permanently)

        if isinstance(entities, EntityIterator):
            raise LOGSException(
                "An %a cannot be used for delete. Please convert it to a list first."
                % EntityIterator.__name__
            )
        elif not isinstance(entities, list):
            entities = [entities]
        return decorator(entities)

    @overload
    def deleteById(self, entityType: Type[Constants.ENTITIES], ids: int):
        ...

    @overload
    def deleteById(self, entityType: Type[Constants.ENTITIES], ids: str):
        ...

    @overload
    def deleteById(self, entityType: Type[Constants.ENTITIES], ids: List[int]):
        ...

    @overload
    def deleteById(self, entityType: Type[Constants.ENTITIES], ids: List[str]):
        ...

    # Implementation of overload
    def deleteById(self, entityType=None, ids: Any = None, permanently: bool = False):
        def decorator(entityType: Any):
            sampleIds: List[Constants.ID_TYPE] = []

            if entityType == Sample and ids:
                sampleIds = ids

            self._deleteEntities(Sample, sampleIds, permanently=permanently)

        if ids and not isinstance(ids, list):
            ids = [ids]
        return decorator(entityType)

    def sample(self, id: int) -> Sample:
        return self._fetchEntity(Sample, id)

    def samples(self, parameter: Optional[SampleRequestParameter] = None) -> Samples:
        if parameter and not isinstance(parameter, SampleRequestParameter):
            raise LOGSException(
                "Parameter for %s.samples must be of type %a. (Got %a)"
                % (
                    type(self).__name__,
                    SampleRequestParameter.__name__,
                    type(parameter).__name__,
                )
            )
        return Samples(connection=self._connection, parameters=parameter)

    def project(self, id: int) -> Project:
        return self._fetchEntity(Project, id)

    def projects(self, parameter: Optional[ProjectRequestParameter] = None) -> Projects:
        if parameter and not isinstance(parameter, ProjectRequestParameter):
            raise LOGSException(
                "Parameter for %s.projects must be of type %a. (Got %a)"
                % (
                    type(self).__name__,
                    ProjectRequestParameter.__name__,
                    type(parameter).__name__,
                )
            )
        return Projects(connection=self._connection, parameters=parameter)

    def dataset(self, id: int) -> Dataset:
        return self._fetchEntity(Dataset, id)

    def datasets(self, parameter: Optional[DatasetRequestParameter] = None) -> Datasets:
        if parameter and not isinstance(parameter, DatasetRequestParameter):
            raise LOGSException(
                "Parameter for %s.datasets must be of type %a. (Got %a)"
                % (
                    type(self).__name__,
                    DatasetRequestParameter.__name__,
                    type(parameter).__name__,
                )
            )
        return Datasets(connection=self._connection, parameters=parameter)

    def document(self, id: int) -> Document:
        return self._fetchEntity(Document, id)

    def documents(
        self, parameter: Optional[DocumentRequestParameter] = None
    ) -> Documents:
        if parameter and not isinstance(parameter, DocumentRequestParameter):
            raise LOGSException(
                "Parameter for %s.documents must be of type %a. (Got %a)"
                % (
                    type(self).__name__,
                    DocumentRequestParameter.__name__,
                    type(parameter).__name__,
                )
            )
        return Documents(connection=self._connection, parameters=parameter)

    def person(self, id: int) -> Person:
        return self._fetchEntity(Person, id)

    def persons(self, parameter: Optional[PersonRequestParameter] = None) -> Persons:
        if parameter and not isinstance(parameter, PersonRequestParameter):
            raise LOGSException(
                "Parameter for %s.persons must be of type %a. (Got %a)"
                % (
                    type(self).__name__,
                    PersonRequestParameter.__name__,
                    type(parameter).__name__,
                )
            )
        return Persons(connection=self._connection, parameters=parameter)

    def method(self, id: int) -> Method:
        return self._fetchEntity(Method, id)

    def methods(self, parameter: Optional[MethodRequestParameter] = None) -> Methods:
        if parameter and not isinstance(parameter, MethodRequestParameter):
            raise LOGSException(
                "Parameter for %s.methods must be of type %a. (Got %a)"
                % (
                    type(self).__name__,
                    MethodRequestParameter.__name__,
                    type(parameter).__name__,
                )
            )
        return Methods(connection=self._connection, parameters=parameter)

    def instrument(self, id: int) -> Instrument:
        return self._fetchEntity(Instrument, id)

    def instruments(
        self, parameter: Optional[InstrumentRequestParameter] = None
    ) -> Instruments:
        if parameter and not isinstance(parameter, InstrumentRequestParameter):
            raise LOGSException(
                "Parameter for %s.instruments must be of type %a. (Got %a)"
                % (
                    type(self).__name__,
                    InstrumentRequestParameter.__name__,
                    type(parameter).__name__,
                )
            )
        return Instruments(connection=self._connection, parameters=parameter)

    def experiment(self, id: int) -> Experiment:
        return self._fetchEntity(Experiment, id)

    def experiments(
        self, parameter: Optional[ExperimentRequestParameter] = None
    ) -> Experiments:
        if parameter and not isinstance(parameter, ExperimentRequestParameter):
            raise LOGSException(
                "Parameter for %s.experiments must be of type %a. (Got %a)"
                % (
                    type(self).__name__,
                    ExperimentRequestParameter.__name__,
                    type(parameter).__name__,
                )
            )
        return Experiments(connection=self._connection, parameters=parameter)

    def origin(self, id: int) -> Origin:
        return self._fetchEntity(Origin, id)

    def origins(self, parameter: Optional[OriginRequestParameter] = None) -> Origins:
        if parameter and not isinstance(parameter, OriginRequestParameter):
            raise LOGSException(
                "Parameter for %s.origins must be of type %a. (Got %a)"
                % (
                    type(self).__name__,
                    OriginRequestParameter.__name__,
                    type(parameter).__name__,
                )
            )
        return Origins(connection=self._connection, parameters=parameter)

    def format(self, id: int) -> Format:
        return self._fetchEntity(Format, id)

    def formats(self, parameter: Optional[FormatRequestParameter] = None) -> Formats:
        if parameter and not isinstance(parameter, FormatRequestParameter):
            raise LOGSException(
                "Parameter for %s.formats must be of type %a. (Got %a)"
                % (
                    type(self).__name__,
                    FormatRequestParameter.__name__,
                    type(parameter).__name__,
                )
            )
        return Formats(connection=self._connection, parameters=parameter)

    def role(self, id: int) -> Role:
        return self._fetchEntity(Role, id)

    def roles(self, parameter: Optional[RoleRequestParameter] = None) -> Roles:
        if parameter and not isinstance(parameter, RoleRequestParameter):
            raise LOGSException(
                "Parameter for %s.Roles must be of type %a. (Got %a)"
                % (
                    type(self).__name__,
                    RoleRequestParameter.__name__,
                    type(parameter).__name__,
                )
            )
        return Roles(connection=self._connection, parameters=parameter)

    def autoloadSource(self, id: int) -> AutoloadSource:
        return self._fetchEntity(AutoloadSource, id)

    def autoloadSources(
        self, parameter: Optional[AutoloadSourceRequestParameter] = None
    ) -> AutoloadSources:
        if parameter and not isinstance(parameter, AutoloadSourceRequestParameter):
            raise LOGSException(
                "Parameter for %s.AutoloadSources must be of type %a. (Got %a)"
                % (
                    type(self).__name__,
                    AutoloadSourceRequestParameter.__name__,
                    type(parameter).__name__,
                )
            )
        return AutoloadSources(connection=self._connection, parameters=parameter)

    def autoloadConfiguration(self, id: int) -> AutoloadConfiguration:
        return self._fetchEntity(AutoloadConfiguration, id)

    def autoloadConfigurations(
        self, parameter: Optional[AutoloadConfigurationRequestParameter] = None
    ) -> AutoloadConfigurations:
        if parameter and not isinstance(
            parameter, AutoloadConfigurationRequestParameter
        ):
            raise LOGSException(
                "Parameter for %s.AutoloadConfigurations must be of type %a. (Got %a)"
                % (
                    type(self).__name__,
                    AutoloadConfigurationRequestParameter.__name__,
                    type(parameter).__name__,
                )
            )
        return AutoloadConfigurations(connection=self._connection, parameters=parameter)

    def labNotebookEntry(self, id: int) -> LabNotebookEntry:
        return self._fetchEntity(LabNotebookEntry, id)

    def labNotebookEntries(
        self, parameter: Optional[LabNotebookEntryRequestParameter] = None
    ) -> LabNotebookEntries:
        if parameter and not isinstance(parameter, LabNotebookEntryRequestParameter):
            raise LOGSException(
                "Parameter for %s.LabNotebookEntries must be of type %a. (Got %a)"
                % (
                    type(self).__name__,
                    LabNotebookEntryRequestParameter.__name__,
                    type(parameter).__name__,
                )
            )
        return LabNotebookEntries(connection=self._connection, parameters=parameter)

    def formatVendor(self, id: int) -> FormatVendor:
        return self._fetchEntity(FormatVendor, id)

    def formatVendors(
        self, parameter: Optional[FormatVendorRequestParameter] = None
    ) -> FormatVendors:
        if parameter and not isinstance(parameter, FormatVendorRequestParameter):
            raise LOGSException(
                "Parameter for %s.Vendors must be of type %a. (Got %a)"
                % (
                    type(self).__name__,
                    FormatVendorRequestParameter.__name__,
                    type(parameter).__name__,
                )
            )
        return FormatVendors(connection=self._connection, parameters=parameter)

    def formatMethod(self, id: int) -> FormatMethod:
        return self._fetchEntity(FormatMethod, id)

    def formatMethods(
        self, parameter: Optional[FormatMethodRequestParameter] = None
    ) -> FormatMethods:
        if parameter and not isinstance(parameter, FormatMethodRequestParameter):
            raise LOGSException(
                "Parameter for %s.Methods must be of type %a. (Got %a)"
                % (
                    type(self).__name__,
                    FormatMethodRequestParameter.__name__,
                    type(parameter).__name__,
                )
            )
        return FormatMethods(connection=self._connection, parameters=parameter)

    def formatInstrument(self, id: int) -> FormatInstrument:
        return self._fetchEntity(FormatInstrument, id)

    def formatInstruments(
        self, parameter: Optional[FormatInstrumentRequestParameter] = None
    ) -> FormatInstruments:
        if parameter and not isinstance(parameter, FormatInstrumentRequestParameter):
            raise LOGSException(
                "Parameter for %s.Instruments must be of type %a. (Got %a)"
                % (
                    type(self).__name__,
                    FormatInstrumentRequestParameter.__name__,
                    type(parameter).__name__,
                )
            )
        return FormatInstruments(connection=self._connection, parameters=parameter)

    def formatFormat(self, id: int) -> FormatFormat:
        return self._fetchEntity(FormatFormat, id)

    def formatFormats(
        self, parameter: Optional[FormatFormatRequestParameter] = None
    ) -> FormatFormats:
        if parameter and not isinstance(parameter, FormatFormatRequestParameter):
            raise LOGSException(
                "Parameter for %s.Formats must be of type %a. (Got %a)"
                % (
                    type(self).__name__,
                    FormatFormatRequestParameter.__name__,
                    type(parameter).__name__,
                )
            )
        return FormatFormats(connection=self._connection, parameters=parameter)

    def entity(self, uid: str):
        return Entities(connection=self._connection).fetch(uid=uid)

    def entities(
        self, parameter: Optional[EntitiesRequestParameter] = None
    ) -> Entities:
        return Entities(connection=self._connection, parameters=parameter)

    def datasetMatching(
        self,
        files: Union[Constants.FILE_TYPE, Sequence[Constants.FILE_TYPE]],
        formatIds: Optional[List[str]] = None,
        ignoreReadErrors=False,
    ) -> DatasetMatching:
        return DatasetMatching(
            connection=self._connection,
            files=files,
            formatIds=formatIds,
            ignoreReadErrors=ignoreReadErrors,
        )

    def updatableDatasetFiles(
        self, files: Sequence[Constants.FILE_TYPE], formatIds: List[str]
    ):
        datasets = Datasets(
            connection=self._connection, parameters=cast(DatasetRequestParameter, {})
        ).findDatasetByFiles(files=files, formatIds=formatIds)
        for dataset in datasets:
            yield DatasetsUpdatableFiles(
                datasetId=dataset.logsId,
                files=[
                    FileEntry(fullPath=file.fullPath, state=file.state)
                    for file in dataset.files
                ],
            )

    @property
    def instanceOrigin(self) -> Origin:
        return Origin(name="LOGS (%s)" % self.group, url=self.url, uid=self.uid)

    @property
    def url(self) -> str:
        return self._connection.url

    @property
    def apiUrl(self) -> str:
        return self._connection.apiUrl

    @property
    def uid(self) -> Optional[UUID]:
        return self._connection.metadata.uid

    @property
    def group(self) -> Optional[str]:
        return self._connection._group

    @property
    def currentUser(self) -> Person:
        return self._currentUser


if __name__ == "__main__":
    api_key = input("Please specify api key: ")
    _url = input("Please specify LOGS url: ")

    # Example input:
    # api_key = "8V6oQ804t2nPgGPDJIk4CuneRI5q48ERUxgEpk+YqXzX9uLuMUySycHkeXP6DefN"
    # url = "http://localhost:900/sandbox"

    logs = LOGS(_url, api_key, verbose=True)
