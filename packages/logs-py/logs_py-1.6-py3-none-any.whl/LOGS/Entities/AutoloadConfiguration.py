from datetime import datetime
from typing import Dict, List, Optional

from LOGS.Auxiliary.Decorators import Endpoint
from LOGS.Auxiliary.Exceptions import EntityAPIException
from LOGS.Auxiliary.MinimalModelGenerator import (
    InstrumentMinimalFromDict,
    MethodMinimalFromDict,
)
from LOGS.Entities.AutoloadConfigurationStatus import AutoloadConfigurationStatus
from LOGS.Entities.Format import Format
from LOGS.Entities.InstrumentMinimal import InstrumentMinimal
from LOGS.Entities.MethodMinimal import MethodMinimal
from LOGS.Entity.EntityWithIntId import EntityWithIntId
from LOGS.Interfaces.ICreationRecord import ICreationRecord
from LOGS.Interfaces.IModificationRecord import IModificationRecord
from LOGS.Interfaces.INamedEntity import INamedEntity


@Endpoint("autoload_configurations")
class AutoloadConfiguration(
    INamedEntity, EntityWithIntId, ICreationRecord, IModificationRecord
):
    _enabled: Optional[bool]
    _autoloadSourceId: Optional[int]
    _formats: Optional[List[str]]
    _directories: Optional[List[str]]
    _intervalInSeconds: Optional[int]
    _method: Optional[MethodMinimal]
    _instrument: Optional[InstrumentMinimal]
    _cutoffDate: Optional[datetime]
    _customImportId: Optional[str]
    _parserDefinitions: Optional[Dict[str, Format]]
    _status: Optional[AutoloadConfigurationStatus]

    def triggerAutoload(self):
        connection, endpoint, id = self._getConnectionData()

        _, errors = connection.getEndpoint(endpoint + [id, "trigger_autoload"])
        if errors:
            raise EntityAPIException(entity=self, errors=errors)

    @property
    def enabled(self) -> Optional[bool]:
        return self._enabled

    @enabled.setter
    def enabled(self, value):
        self._enabled = self.checkAndConvertNullable(value, bool, "enabled")

    @property
    def autoloadSourceId(self) -> Optional[int]:
        return self._autoloadSourceId

    @autoloadSourceId.setter
    def autoloadSourceId(self, value):
        self._autoloadSourceId = self.checkAndConvertNullable(
            value, int, "autoloadSourceId"
        )

    @property
    def formats(self) -> Optional[List[str]]:
        return self._formats

    @formats.setter
    def formats(self, value):
        self._formats = self.checkListAndConvertNullable(value, str, "formats")

    @property
    def directories(self) -> Optional[List[str]]:
        return self._directories

    @directories.setter
    def directories(self, value):
        self._directories = self.checkListAndConvertNullable(value, str, "directories")

    @property
    def intervalInSeconds(self) -> Optional[int]:
        return self._intervalInSeconds

    @intervalInSeconds.setter
    def intervalInSeconds(self, value):
        self._intervalInSeconds = self.checkAndConvertNullable(
            value, int, "intervalInSeconds"
        )

    @property
    def method(self) -> Optional[MethodMinimal]:
        return self._method

    @method.setter
    def method(self, value):
        self._method = MethodMinimalFromDict(value, "method", self.connection)

    @property
    def instrument(self) -> Optional[InstrumentMinimal]:
        return self._instrument

    @instrument.setter
    def instrument(self, value):
        self._instrument = InstrumentMinimalFromDict(
            value, "instrument", self.connection
        )

    @property
    def cutoffDate(self) -> Optional[datetime]:
        return self._cutoffDate

    @cutoffDate.setter
    def cutoffDate(self, value):
        self._cutoffDate = self.checkAndConvertNullable(value, datetime, "cutoffDate")

    @property
    def customImportId(self) -> Optional[str]:
        return self._customImportId

    @customImportId.setter
    def customImportId(self, value):
        self._customImportId = self.checkAndConvertNullable(
            value, str, "customImportId"
        )

    @property
    def status(self) -> Optional[AutoloadConfigurationStatus]:
        return self._status

    @status.setter
    def status(self, value):
        self._status = self.checkAndConvertNullable(
            value, AutoloadConfigurationStatus, "status"
        )
