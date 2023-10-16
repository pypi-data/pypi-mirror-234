from typing import TYPE_CHECKING, List, Optional, TypeVar, Union, cast

from LOGS.Auxiliary.Constants import Constants
from LOGS.Auxiliary.Tools import Tools

if TYPE_CHECKING:
    from LOGS.Entity.ConnectedEntity import ConnectedEntity
    from LOGS.Entity.Entity import Entity


def formatErrorMessage(errors: List[str], indent: str = " " * 2):
    indent *= 2
    if len(errors) == 1:
        return errors[0]
    if len(errors) > 1:
        return "\n" + indent + ("\n" + indent).join(errors)
        # return ("\n" + indent).join(errors)
    else:
        return ""


class LOGSException(Exception):
    def __init__(self, message: Optional[Union[List[str], str]] = None):
        if message:
            if isinstance(message, list):
                message = formatErrorMessage(message)
            message = cast(str, message)
            super().__init__(Tools.convertToNativeNewline(message))
        else:
            super().__init__()

    @classmethod
    def gerundVerb(cls, verb: str):
        if verb.endswith("ing"):
            return verb
        elif verb.endswith("e"):
            verb = verb[:-1]

        return verb + "ing"


TEntity = TypeVar("TEntity", bound="Entity")


class LOGSMultilineException(LOGSException):
    def __init__(
        self,
        errors: Optional[List[str]] = None,
        message: Optional[str] = None,
    ):
        if message:
            super().__init__(message)

        super().__init__(self._createMessage(errors=errors))

    @classmethod
    def _createMessage(
        cls,
        errors: Optional[List[str]] = None,
    ):
        pass

        indent = " " * 4
        message = ""

        indent *= 2

        if errors:
            message = errors.pop(0)

        if errors:
            message += "\n" + indent + ("\n" + indent).join(errors)

        return message


class EntityIncompleteException(LOGSException):
    def __init__(
        self,
        entity: Union["Entity", "ConnectedEntity"],
        errors: Optional[List[str]] = None,
        message: Optional[str] = None,
    ):
        if message:
            super().__init__(message)

        super().__init__(self._createMessage(entity=entity, errors=errors))

    def _createMessage(
        self,
        entity: Union["Entity", "ConnectedEntity"],
        errors: Optional[List[str]] = None,
    ):
        pass

        indent = " " * 2
        message = ""

        message = "Entity %a is incomplete please fetch full entity" % (
            entity.identifier
        )

        indent *= 2
        if errors:
            message += formatErrorMessage(errors=errors, indent=indent)
            # lines = errors.split("\n")
            # if len(lines) > 1:
            #     message += ":\n" + indent + ("\n" + indent).join(lines)
            # else:
            #     message += ": " + errors
        else:
            message += "."

        return message


class EntityAPIException(LOGSException):
    _action = "communicate"

    def __init__(
        self,
        entity: Optional[Union[TEntity, List[TEntity]]] = None,
        errors: Optional[List[str]] = None,
        message: Optional[str] = None,
    ):
        if message:
            super().__init__(message)

        super().__init__(self._createMessage(entity=entity, errors=errors))

    def _createMessage(
        self,
        entity: Optional[Union[TEntity, List[TEntity]]],
        errors: Optional[List[str]] = None,
    ):
        from LOGS.Entity.Entity import Entity

        indent = " " * 2
        message = ""
        if isinstance(entity, list):
            message = "%sCould not %s %s %a" % (
                "\n" + indent if errors and len(errors) > 1 else "",
                self._action,
                Tools.plural("entity", entity),
                Tools.eclipsesJoin(", ", [e.identifier for e in entity]),
            )
        elif isinstance(entity, Entity):
            message = "Could not %s entity %a" % (self._action, entity.identifier)
        else:
            message = "%s entity failed" % self.gerundVerb(self._action.capitalize())

        # indent *= 2
        if errors:
            message += ": " + formatErrorMessage(errors=errors, indent=indent)
            # lines = error.split("\n")
            # if len(lines) > 1:
            #     message += ":\n" + indent + ("\n" + indent).join(lines)
            # else:
            #     message += ": " + error
        else:
            message += "."

        return message


class EntityFetchingException(EntityAPIException):
    _action = "fetch"


class EntityUpdatingException(EntityAPIException):
    _action = "update"


class EntityCreatingException(EntityAPIException):
    _action = "create"


class EntityDeletingException(LOGSException):
    _action = "delete"

    def __init__(
        self,
        entityIds: Optional[Union[Constants.ID_TYPE, List[Constants.ID_TYPE]]] = None,
        errors: Optional[List[str]] = None,
        message: Optional[str] = None,
    ):
        if message:
            super().__init__(message)

        super().__init__(self._createMessage(entityIds=entityIds, errors=errors))

    def _createMessage(
        self,
        entityIds: Optional[Union[Constants.ID_TYPE, List[Constants.ID_TYPE]]],
        errors: Optional[List[str]] = None,
    ):
        from LOGS.Entity.Entity import Entity

        indent = " " * 2
        message = ""
        if isinstance(entityIds, list):
            message = "%sCould not %s %s %a" % (
                "\n" + indent if errors and len(errors) > 1 else "",
                self._action,
                Tools.plural("entity", entityIds),
                Tools.eclipsesJoin(", ", [str(id) for id in entityIds]),
            )
        elif isinstance(entityIds, Entity):
            message = "Could not %s entity %a" % (self._action, entityIds.identifier)
        else:
            message = "%s entity failed" % (self._action.capitalize() + "ing")

        indent *= 2
        if errors:
            message += ": " + formatErrorMessage(errors=errors, indent=indent)
            # lines = error.split("\n")
            # if len(lines) > 1:
            #     message += ":\n" + indent + ("\n" + indent).join(lines)
            # else:
            #     message += ": " + error
        else:
            message += "."

        return message


class EntityNotFoundException(LOGSException):
    def __init__(self, entity=None):
        ident = ""
        if entity:
            ident = " " + str(entity.id)
            name = entity.name
            if name:
                ident += " " + name
            ident += " (id:%s)" % str(entity.id)

        super().__init__("%s%s is not connected." % (type(entity).__name__, ident))


class NotConnectedException(LOGSException):
    def __init__(self, message: Optional[str] = None):
        if message:
            super().__init__(message=message)
        else:
            super().__init__("Not connected.")


class EntityNotConnectedException(NotConnectedException):
    def __init__(
        self,
        entity: Optional["ConnectedEntity"] = None,
        identifier: Optional[str] = None,
    ):
        if entity:
            super().__init__("Entity %a is not connected." % (entity.identifier))
        elif identifier:
            super().__init__("Entity %a is not connected." % (identifier))
        else:
            super().__init__("Entity is not connected.")
