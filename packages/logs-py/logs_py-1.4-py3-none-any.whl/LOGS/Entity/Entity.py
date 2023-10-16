from typing import Any, Optional, cast

from LOGS.Auxiliary import MinimalModelGenerator
from LOGS.Auxiliary.Constants import Constants
from LOGS.Auxiliary.Exceptions import (
    EntityDeletingException,
    EntityFetchingException,
    EntityNotFoundException,
    EntityUpdatingException,
)
from LOGS.Entity.ConnectedEntity import ConnectedEntity
from LOGS.Entity.EntityRequestParameter import EntityRequestParameter
from LOGS.LOGSConnection import LOGSConnection

# SELF = TypeVar("SELF", bound="Entity")


class Entity(ConnectedEntity):
    _id: Constants.ID_TYPE
    _defaultRequestParameter: dict = EntityRequestParameter().toDict()

    def __init__(
        self,
        ref=None,
        id: Optional[Constants.ID_TYPE] = None,
        connection: Optional[LOGSConnection] = None,
    ):
        """Represents a connected LOGS entity type"""
        if id:
            self._id = id

        super().__init__(ref=ref, connection=connection)

    def _getConnectionData(self):
        if not self._endpoint:
            raise NotImplementedError(
                "Endpoint missing for of entity type %a."
                % (
                    type(self).__name__
                    if type(self).__name__ != Entity.__name__
                    else "unknown"
                )
            )

        if not self.id:
            raise EntityNotFoundException(self)

        return self._getConnection(), self._endpoint, self.id

    def __str__(self):
        s = (" name:'%s'" % getattr(self, "name")) if hasattr(self, "name") else ""
        return "<%s id:%s%s>" % (type(self).__name__, str(self.id), s)

    def getUIUrl(self) -> str:
        if not self._uiEndpoint:
            raise NotImplementedError(
                "No UI endpoint specified for entity type %a."
                % (
                    type(self).__name__
                    if type(self).__name__ != Entity.__name__
                    else "unknown"
                )
            )
        connection = self._getConnection()

        return connection.getUIEndpointUrl(self._uiEndpoint + [str(self.id)])

    def _fetchEntity(self, connection: LOGSConnection):
        if not self._endpoint:
            raise NotImplementedError(
                "Fetching of entity type %a is not implemented."
                % (
                    type(self).__name__
                    if type(self).__name__ != Entity.__name__
                    else "unknown"
                )
            )

        ref, errors = connection.getEndpoint(
            cast(Any, self._endpoint + [str(self.id)]), self._defaultRequestParameter
        )
        if errors:
            raise EntityFetchingException(entity=self, errors=errors)

        self._fromRef(ref, type(self))
        for k in self.__dict__:
            a = getattr(self, k)
            if issubclass(type(a), ConnectedEntity):
                cast(ConnectedEntity, a).connection = self.connection

    def fetch(self):
        self._fetchEntity(self._getConnection())

    def _updateEntity(self, connection: LOGSConnection):
        if not self._endpoint:
            raise NotImplementedError(
                "Updating of entity type %a is not implemented."
                % (
                    type(self).__name__
                    if type(self).__name__ != Entity.__name__
                    else "unknown"
                )
            )

        if not self.id:
            raise EntityNotFoundException(self)

        data, errors = connection.putEndpoint(
            self._endpoint + [self.id], data=self.toDict()
        )
        if errors:
            raise EntityUpdatingException(entity=self, errors=errors)

        self.override(data)

    def _deleteEntity(self, connection: LOGSConnection, permanently: bool = False):
        if not self._endpoint:
            raise NotImplementedError(
                "Deleting of entity type %a is not implemented."
                % (
                    type(self).__name__
                    if type(self).__name__ != Entity.__name__
                    else "unknown"
                )
            )

        if not self.id:
            raise EntityNotFoundException(self)

        _, error = connection.deleteEndpoint(
            self._endpoint + [self.id], parameters={"deletePermanently": permanently}
        )
        if permanently:
            self.connection = None

        if error:
            if [e for e in error if "Soft-Delete is not supported" in e]:
                raise EntityDeletingException(
                    entityIds=self.id,
                    errors=[
                        "This entity cannot be trashed.",
                        "Please use 'permanently = true' parameter.",
                    ],
                )
            else:
                raise EntityDeletingException(entityIds=self.id, errors=error)

    def update(self):
        self._updateEntity(self._getConnection())

    def delete(self, permanently: bool = False):
        self._deleteEntity(self._getConnection(), permanently=permanently)

    def toMinimal(self):
        return MinimalModelGenerator.MinimalFromSingle(
            self.toDict(), type(self).__name__, connection=self.connection
        )

    @property
    def identifier(self):
        name = self.name
        return "%s(id:%s)%s" % (
            type(self).__name__,
            str(self.id),
            "'" + name + "'" if name else "",
        )

    @property
    def name(self):
        return getattr(self, "_name") if hasattr(self, "_name") else None

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        self._id = value
