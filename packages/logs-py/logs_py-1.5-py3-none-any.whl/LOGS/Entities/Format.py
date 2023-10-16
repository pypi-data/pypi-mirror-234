from typing import List, Optional

from LOGS.Auxiliary.Decorators import Endpoint
from LOGS.Entities.FormatMetaData import FormatMetaData
from LOGS.Entity.EntityWithStrId import EntityWithStrId
from LOGS.Interfaces.INamedEntity import INamedEntity
from LOGS.LOGSConnection import LOGSConnection


@Endpoint("parsers")
class Format(INamedEntity, EntityWithStrId):
    _version: str
    _vendors: List[str]
    _methods: List[str]
    _formats: List[str]
    _instruments: List[str]
    _metaData: List[FormatMetaData]

    def __init__(
        self,
        ref=None,
        id: Optional[str] = None,
        connection: Optional[LOGSConnection] = None,
    ):
        """Represents a connected LOGS entity type"""

        self._version = "0.0"
        self._vendors = []
        self._methods = []
        self._formats = []
        self._instruments = []
        self._metaData = []

        super().__init__(ref=ref, id=id, connection=connection)

    def fromDict(self, ref, formatDict=None) -> None:
        if isinstance(ref, dict):
            if "metaData" in ref and isinstance(ref["metaData"], list):
                ref["vendors"] = []
                ref["methods"] = []
                ref["instruments"] = []
                ref["formats"] = []
                for metaData in ref["metaData"]:
                    if metaData["vendor"]:
                        ref["vendors"].extend(v["name"] for v in metaData["vendor"])
                    if metaData["method"]:
                        ref["methods"].extend(v["name"] for v in metaData["method"])
                    if metaData["instrument"]:
                        ref["instruments"].extend(
                            v["name"] for v in metaData["instrument"]
                        )
                    if metaData["format"]:
                        ref["formats"].extend(v["name"] for v in metaData["format"])

            if "majorVersion" in ref and "minorVersion" in ref:
                ref["version"] = "%s.%s" % (ref["majorVersion"], ref["minorVersion"])
        super().fromDict(ref=ref, formatDict=formatDict)

    def toDict(self):
        d = super().toDict()

        if self.version:
            d["majorVersion"], d["minorVersion"] = [
                int(v) for v in self.version.split(".")
            ]
            del d["version"]

        return d

    @property
    def version(self) -> Optional[str]:
        return self._version

    @version.setter
    def version(self, value):
        self._version = self.checkAndConvert(value, str, "version")

    @property
    def vendors(self) -> List[str]:
        return self._vendors

    @vendors.setter
    def vendors(self, value):
        self._vendors = self.checkListAndConvert(value, str, "vendors")

    @property
    def methods(self) -> List[str]:
        return self._methods

    @methods.setter
    def methods(self, value):
        self._methods = self.checkListAndConvert(value, str, "methods")

    @property
    def formats(self) -> List[str]:
        return self._formats

    @formats.setter
    def formats(self, value):
        self._formats = self.checkListAndConvert(value, str, "formats")

    @property
    def instruments(self) -> List[str]:
        return self._instruments

    @instruments.setter
    def instruments(self, value):
        self._instruments = self.checkListAndConvert(value, str, "instruments")

    @property
    def metaData(self) -> List[FormatMetaData]:
        return self._metaData

    @metaData.setter
    def metaData(self, value):
        self._metaData = self.checkListAndConvert(
            value,
            FormatMetaData,
            "metaData",
            converter=lambda ref: FormatMetaData(ref, connection=self.connection),
        )
