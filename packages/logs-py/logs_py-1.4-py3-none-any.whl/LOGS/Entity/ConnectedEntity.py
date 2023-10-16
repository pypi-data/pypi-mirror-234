from typing import List, Optional, cast

from LOGS.Auxiliary.Exceptions import EntityNotConnectedException
from LOGS.Entity.SerializeableContent import SerializeableContent
from LOGS.LOGSConnection import LOGSConnection


class ConnectedEntity(SerializeableContent):
    _connection: Optional[LOGSConnection]
    _endpoint: Optional[List[str]] = None
    _uiEndpoint: Optional[List[str]] = None
    _noSerialize = ["connection"]

    def __init__(self, ref=None, connection: Optional[LOGSConnection] = None):
        self._connection = connection

        if not self._uiEndpoint and self._endpoint and len(self._endpoint) == 1:
            self._uiEndpoint = ["#" + self._endpoint[0]]

        super().__init__(ref=ref)

    def _getConnection(self):
        if not self._connection:
            raise EntityNotConnectedException(self)
        return self._connection

    @property
    def connection(self) -> Optional[LOGSConnection]:
        return self._connection

    @connection.setter
    def connection(self, value):
        self._connection = self.checkAndConvertNullable(
            value, LOGSConnection, "connection"
        )
        # print("set connection %a -> %a" % (type(self).__name__, type(self.connection).__name__))
        for k in self.__dict__:
            a = getattr(self, k)
            if issubclass(type(a), ConnectedEntity):
                # print("  => set connection %a" % (type(a).__name__, type(self.connection).__name__))
                cast(ConnectedEntity, a).connection = self.connection

    @property
    def identifier(self):
        return "%s" % (type(self).__name__)
