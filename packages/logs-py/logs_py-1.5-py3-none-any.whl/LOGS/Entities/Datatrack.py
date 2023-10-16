from typing import Any, List, Literal, Optional, cast

import numpy as np

from LOGS.Auxiliary.Exceptions import (
    EntityIncompleteException,
    LOGSException,
    formatErrorMessage,
)
from LOGS.Entity.ConnectedEntity import ConnectedEntity
from LOGS.LOGSConnection import ResponseTypes

NumberTypeType = Literal["int", "float", "double"]
DatatrackType = Literal[
    "binary", "char", "formatted_table", "image", "numeric_array", "numeric_matrix"
]
CodecType = Literal["char", "jpeg", "points", "generator"]


class Datatrack(ConnectedEntity):
    _type: Optional[DatatrackType] = None
    _codec: Optional[CodecType] = None
    _id: Optional[str] = None
    _count: Optional[int] = None
    _size: Optional[List[int]] = None
    _min: Optional[List[float]] = None
    _max: Optional[List[float]] = None
    _numberType: Optional[NumberTypeType] = None
    _data: Optional[Any] = None
    _incomplete = True

    def _getConnectionData(self):
        if not self._endpoint:
            raise NotImplementedError(
                "Endpoint missing for of entity type %a." % (type(self).__name__)
            )

        if not self.id:
            raise LOGSException("%s id is not defined." % type(self).__name__)

        return self._getConnection(), self._endpoint, self.id

    def _fetchData(self):
        connection, endpoint, id = self._getConnectionData()

        data, errors = connection.getEndpoint(
            endpoint + [id], responseType=ResponseTypes.RAW
        )
        if errors:
            raise LOGSException(
                "Could not fetch %s: %s"
                % (type(self).__name__, formatErrorMessage(errors))
            )

        self._data = data

    def fetchFull(self):
        self._fetchData()
        self._incomplete = False

    def __iter__(self):
        if self._incomplete:
            raise EntityIncompleteException(self)
        if self._data is not None:
            for x in self._data:
                yield x

    @property
    def type(self) -> Optional[DatatrackType]:
        return self._type

    @type.setter
    def type(self, value):
        self._type = cast(Any, self.checkAndConvertNullable(value, str, "type"))

    @property
    def codec(self) -> Optional[CodecType]:
        return self._codec

    @codec.setter
    def codec(self, value):
        self._codec = cast(Any, self.checkAndConvertNullable(value, str, "codec"))

    @property
    def id(self) -> Optional[str]:
        return self._id

    @id.setter
    def id(self, value):
        self._id = self.checkAndConvertNullable(value, str, "id")

    @property
    def count(self) -> Optional[int]:
        return self._count

    @count.setter
    def count(self, value):
        self._count = self.checkAndConvertNullable(value, int, "count")

    @property
    def size(self) -> Optional[List[int]]:
        return self._size

    @size.setter
    def size(self, value):
        self._size = self.checkListAndConvertNullable(value, int, "size")

    @property
    def min(self) -> Optional[List[float]]:
        return self._min

    @min.setter
    def min(self, value):
        self._min = self.checkListAndConvertNullable(value, float, "min")

    @property
    def max(self) -> Optional[List[float]]:
        return self._max

    @max.setter
    def max(self, value):
        self._max = self.checkListAndConvertNullable(value, float, "max")

    @property
    def numberType(self) -> Optional[NumberTypeType]:
        return self._numberType

    @numberType.setter
    def numberType(self, value):
        self._numberType = cast(
            Any, self.checkAndConvertNullable(value, str, "numberType")
        )

    @property
    def data(self) -> Optional[np.ndarray]:
        if self._incomplete:
            raise EntityIncompleteException(self)
        return self._data
