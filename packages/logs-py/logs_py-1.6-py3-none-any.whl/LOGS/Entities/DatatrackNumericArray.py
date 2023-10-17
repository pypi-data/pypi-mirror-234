from typing import Literal, Optional, cast

import numpy as np

from LOGS.Auxiliary.Exceptions import (
    EntityIncompleteException,
    LOGSException,
    formatErrorMessage,
)
from LOGS.Entities.Datatrack import Datatrack
from LOGS.LOGSConnection import ResponseTypes

NumberTypeType = Literal["int", "float", "double"]
DatatrackType = Literal[
    "binary", "char", "formatted_table", "image", "numeric_array", "numeric_matrix"
]
CodecType = Literal["char", "jpeg", "points", "generator"]


class DatatrackNumericArray(Datatrack):
    _data: Optional[np.ndarray] = None

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

        self._data = np.frombuffer(cast(bytes, data), dtype=np.double)

    def __iter__(self):
        if self._incomplete:
            raise EntityIncompleteException(self)
        if self._data is not None:
            for x in self._data:
                yield x

    @property
    def data(self) -> Optional[np.ndarray]:
        if self._incomplete:
            raise EntityIncompleteException(self)
        return self._data
