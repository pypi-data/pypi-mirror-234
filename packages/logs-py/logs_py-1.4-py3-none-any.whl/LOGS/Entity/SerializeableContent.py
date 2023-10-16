import inspect
import json
import math
import random
from copy import deepcopy
from datetime import datetime
from enum import Enum
from typing import (
    Any,
    Callable,
    Dict,
    List,
    Optional,
    Tuple,
    Type,
    TypeVar,
    Union,
    cast,
)
from uuid import UUID

import numpy as np

from LOGS.Auxiliary.Constants import Constants
from LOGS.Auxiliary.Exceptions import EntityIncompleteException
from LOGS.Auxiliary.ReplaceMessage import ReplaceMessage
from LOGS.Auxiliary.Tools import Tools

_T = TypeVar("_T")


class SerializeableContent:
    _noSerialize: List[str] = []
    _typeMapper: Optional[Dict[str, Any]] = None
    _planeClass = False

    def __init__(self, ref=None):
        if ref != None:
            self._fromRef(ref=ref, selfClass=type(self))

    def override(self, ref):
        self._fromRef(ref=ref, selfClass=type(self))

    def _fromRef(
        self,
        ref,
        selfClass,
        fromInstance=None,
        fromDict=None,
        formatDict=None,
        convertOtherType: Optional[Tuple[type, Callable[[Any], Any]]] = None,
    ):
        # print("FromRef", selfClass.__name__, self._json_schema)

        # if not isinstance(ref, (selfClass, dict)) and convertOtherType:
        #     ref = convertOtherType(ref)
        if convertOtherType and isinstance(ref, convertOtherType[0]):
            ref = convertOtherType[1](ref)

        if isinstance(ref, selfClass):
            if fromInstance:
                fromInstance(ref)
            else:
                self.fromInstance(ref)
        elif isinstance(ref, dict):
            if hasattr(self, "_typeMapper") and self._typeMapper:
                for k, t in self._typeMapper.items():
                    if k in ref:
                        if isinstance(ref[k], list):
                            self.checkFieldAndConvertToList(
                                ref, fieldName=k, fieldType=t
                            )
                        else:
                            self.checkFieldAndConvert(
                                ref, fieldName=k, fieldType=t, allowNone=True
                            )

            if fromDict:
                fromDict(ref)
            else:
                self.fromDict(ref, formatDict=formatDict)
        else:
            types: List[type] = [dict, type(self)]
            if convertOtherType:
                if isinstance(convertOtherType[0], (tuple, list)):
                    types.extend(convertOtherType[0])
                else:
                    types.append(convertOtherType[0])
            raise Exception(
                "%s instance cannot be derived from type %a. (Expected one of %s)"
                % (
                    selfClass.__name__,
                    type(ref).__name__,
                    ", ".join([f"'{t.__name__}'" for t in types]),
                )
            )

    def fromInstance(self, ref):
        attrList = self._getAttrList()
        for k in attrList:
            if hasattr(ref, k):
                setattr(self, k, getattr(ref, k))

    def fromDict(self, ref, formatDict=None) -> None:
        if formatDict:
            ref = deepcopy(ref)
            ref = formatDict(ref)
            if ref == None:
                ref = {}

        # if "type" in ref:
        #     self.type = ref["type"]

        # self.validateDict(ref)
        # print("ref", ref)
        # print("ref", type(self).__name__)

        for k in dir(self):
            # _k = "_" + k
            if k in ref and hasattr(self, k) and not callable(getattr(self, k)):
                try:
                    # print("  ", k, "->", ref[k])
                    setattr(self, k, ref[k])
                except AttributeError:
                    # print("ERROR:", k, "->", ref[k])
                    pass

        # This is the old way to check if settable: checks if a private attr exists and sets this
        # setattr(self, k, [])
        # if hasattr(self, _k) and not callable(getattr(self, _k)) and k in ref:
        #     print(k, "->", ref[k])
        #     setattr(self, _k, ref[k])

    @classmethod
    def toBaseclassString(cls, obj):
        if isinstance(obj, SerializeableContent):
            return obj.toString()
        if isinstance(obj, dict):
            return "<%s>" % obj["type"] if "type" in obj else "unknown"
        return "<%s>" % type(obj).__name__

    def toString(self):
        return str(self)

    @classmethod
    def _serializeItem(cls, item):
        # print("serialize", item, hasattr(item, "__dict__"))
        if hasattr(item, "toDict"):
            return item.toDict()
        if isinstance(item, cast(Any, np.float32)):
            return item.item()
        elif hasattr(
            item, "__dict__"
        ):  # check if it is a defined class -> is this robust?
            return None
        elif isinstance(item, UUID):
            return str(item)
        elif isinstance(
            item, float
        ):  # check if it is a defined class -> is this robust?
            if math.isnan(item):
                item = 0
            elif math.isinf(item):
                item = 0
            return item
        else:
            return item

    def _getAttrList(self):
        result = None
        if self._planeClass:
            result = [
                a[0]
                for a in inspect.getmembers(self, lambda a: not inspect.isroutine(a))
                if a[0][0] != "_"
            ]
        else:
            realAttributes = [
                a[1:]
                for a in dir(self)
                if a[0] == "_" and hasattr(self, a) and not callable(getattr(self, a))
            ]

            result = []
            for a in realAttributes:
                try:
                    if hasattr(self, a):
                        result.append(a)
                except (
                    EntityIncompleteException
                ):  # while serializing we want to ignore incomplete fields
                    pass

        return result

    def toDict(self) -> Dict[str, Any]:
        # print("toDict", type(self).__name__)
        if not hasattr(self, "_noSerialize"):
            self._noSerialize = []
        d = {}

        attrList = self._getAttrList()

        for k in attrList:
            if k in self._noSerialize:
                continue

            a = getattr(self, k)
            # print("attr", k, "->", a, "=>", type(a).__name__)
            if isinstance(a, (list, np.ndarray)):
                l: Any = []
                for e in a:
                    l.append(self._serializeItem(e))
                d[k] = l
            elif isinstance(a, dict):
                l = {}
                for i, v in a.items():
                    l[i] = self._serializeItem(v)
                d[k] = l
            elif isinstance(a, datetime):
                # if not a.tzinfo:
                #     a.replace(tzinfo=tzlocal.get_localzone())
                # print(">>>", a.strftime("%Y-%m-%dT%H:%M:%S.%fZ"))
                # print(">>>", a.strftime("%Y-%m-%dT%H:%M:%S"))
                # d[k] = a.isoformat() + ".000Z"
                d[k] = a.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
                # d[k] = "2021-12-01T00:00:00.000Z"
            elif isinstance(a, Enum):
                d[k] = a.value
            elif a != None:
                d[k] = self._serializeItem(a)

        return d

    @classmethod
    def _objectDictToDict(cls, item):
        # print("  item", item)
        if isinstance(item, dict):
            d = {}
            for k, v in item.items():
                # item[k] = cls._objectDictToDict(v)
                d[k] = cls._objectDictToDict(v)
            return d
        if isinstance(item, list):
            l = []
            for v in item:
                # item[k] = cls._objectDictToDict(v)
                l.append(cls._objectDictToDict(v))
            return l
        else:
            if hasattr(item, "toDict") and callable(getattr(item, "toDict")):
                return item.toDict()

        return item

    @classmethod
    def _dictToJson(cls, dict, indent=2, sort_keys=True, compact=False):
        separators = None
        if compact:
            indent = None
            separators = (",", ":")
        return json.dumps(
            dict, indent=indent, sort_keys=sort_keys, separators=separators
        )

    def toJson(self, indent=2, sort_keys=True, compact=False, validate=False):
        return self._dictToJson(
            self.toDict(), indent=indent, sort_keys=sort_keys, compact=compact
        )

    def printJson(self, validate=False):
        print(self.toJson(validate=validate))

    @classmethod
    def truncString(cls, text: str, length: int = 30) -> str:
        return Tools.truncString(text=text, length=length)

    @staticmethod
    def delEntryFromDict(d: dict, entry: str):
        if entry in d:
            del d[entry]

    def dictToString(self, element, length=30):
        text = ""
        if "name" in element:
            text = "Name: " + str(element["name"])

        return self.truncString(text, length=length)

    @classmethod
    def plural(cls, word, count):
        if isinstance(count, list):
            count = len(count)

        if word[-1] == "y" and count > 1:
            word = word[:-1] + "ie"

        return word + ("s" if count > 1 else "")

    def createOnDemand(self, attr: str, typeOfValue: type):
        if getattr(self, attr) == None:
            setattr(self, attr, typeOfValue())

        return getattr(self, attr)

    @classmethod
    def checkAndConvertNullable(
        cls,
        value: Any,
        fieldType: Union[Type[_T], List[Type[_T]]],
        fieldName: Optional[str] = None,
        converter: Optional[Callable[[Any], _T]] = None,
    ):
        return cls.checkAndConvert(
            value=value,
            fieldType=fieldType,
            fieldName=fieldName,
            converter=converter,
            allowNone=True,
        )

    @classmethod
    def checkAndConvert(
        cls,
        value: Any,
        fieldType: Union[Type[_T], List[Type[_T]]],
        fieldName: Optional[str] = None,
        converter: Optional[Callable[[Any], _T]] = None,
        allowNone=False,
    ) -> _T:
        if (
            inspect.isclass(fieldType)
            and issubclass(fieldType, SerializeableContent)
            and isinstance(value, dict)
        ):
            return cast(Any, fieldType)(ref=value)
        return cast(
            _T,
            Tools.checkAndConvert(
                value=value,
                fieldType=cast(Any, fieldType),
                fieldName=fieldName,
                converter=converter,
                allowNone=allowNone,
            ),
        )

    @classmethod
    def checkFieldAndConvert(
        cls,
        elements: Dict[str, Any],
        fieldType: Union[Type[_T], List[Type[_T]]],
        fieldName: Optional[str] = None,
        converter: Optional[Callable[[Any], _T]] = None,
        allowNone=False,
    ):
        if fieldName in elements:
            elements[fieldName] = cls.checkAndConvert(
                elements[fieldName],
                fieldType=fieldType,
                fieldName=fieldName,
                converter=converter,
                allowNone=allowNone,
            )

    @classmethod
    def checkFieldAndConvertToList(
        cls,
        elements: Dict[str, Any],
        fieldType: Union[Type[_T], List[Type[_T]]],
        fieldName: Optional[str] = None,
        converter: Optional[Callable[[Any], _T]] = None,
        allowNone: bool = False,
        singleToList: bool = False,
        length: int = -1,
    ):
        if fieldName in elements:
            elements[fieldName] = cls.checkListAndConvert(
                elements[fieldName],
                fieldType=fieldType,
                fieldName=fieldName,
                converter=converter,
                allowNone=allowNone,
                singleToList=singleToList,
                length=length,
            )

    @classmethod
    def checkListAndConvertNullable(
        cls,
        value: Any,
        fieldType: Union[Type[_T], List[Type[_T]]],
        fieldName: Optional[str] = None,
        converter: Optional[Callable[[Any], _T]] = None,
        length: int = -1,
    ):
        return cls.checkListAndConvert(
            value=value,
            fieldType=fieldType,
            fieldName=fieldName,
            converter=converter,
            length=length,
            singleToList=True,
            allowNone=True,
        )

    @classmethod
    def checkListAndConvert(
        cls,
        value: Any,
        fieldType: Union[Type[_T], List[Type[_T]]],
        fieldName: Optional[str] = None,
        converter: Optional[Callable[[Any], _T]] = None,
        allowNone: bool = False,
        singleToList: bool = False,
        length: int = -1,
    ) -> List[_T]:
        return Tools.checkListAndConvert(
            value=value,
            fieldType=fieldType,
            fieldName=fieldName,
            converter=converter,
            allowNone=allowNone,
            singleToList=singleToList,
            length=length,
        )

    @classmethod
    def checkAndAppend(
        cls,
        value: Any,
        fieldType: Type[_T],
        fieldName: Optional[str] = None,
        converter: Optional[Callable[[Any], _T]] = None,
        allowNone: bool = False,
    ):
        if not converter:
            converter = fieldType

        if value == None:
            value = []

        if fieldName == None:
            fieldName = "field"
        fieldName = cast(str, fieldName)

        if not isinstance(value, list):
            raise Exception(
                "%s must be of type 'list'. (Got type %a)"
                % (fieldName.capitalize(), type(value).__name__)
            )

        return [
            cls.checkAndConvert(
                f,
                fieldName=fieldName,
                fieldType=fieldType,
                converter=converter,
                allowNone=allowNone,
            )
            for f in value
        ]

    def checkInstance(self, instance, path: List[str] = []):
        # print("check", path, instance)
        if isinstance(instance, SerializeableContent):
            instance.check(path)

    def checkProperty(self, property: str, path: List[str] = []):
        if hasattr(self, property):
            item = getattr(self, property)
            if isinstance(item, list):
                for k, v in enumerate(item):
                    self.checkInstance(v, path + [str(self), "%s[%d]" % (property, k)])
            elif isinstance(item, dict):
                for k, v in item.items():
                    self.checkInstance(v, path + [str(self), "%s[%s]" % (property, k)])
            else:
                self.checkInstance(item, path + [str(self), "%s" % (property)])

    def check(self, path: List[str] = []):
        for k in dir(self):
            if hasattr(self, k) and not callable(getattr(self, k)) and k[0] != "_":
                self.checkProperty(k, path)

    def __str__(self):
        return "<%s>" % (type(self).__name__)

    @classmethod
    def replaceControlCharacters(
        cls,
        text: Optional[Union[str, Dict[str, str], List[str]]],
        excludeCharacters: List[str] = [],
        mergeMessages: bool = False,
        excludeKeys: List[str] = [],
    ):
        if text is None:
            return "", [ReplaceMessage(message="No text defined")]

        messages: List[ReplaceMessage] = []

        if isinstance(text, dict):
            if (
                "type" in text
                and text["type"] == "parameter"
                and "multiline" in text
                and text["multiline"]
            ):
                excludeCharacters.append("line feed")
            for k in text.keys():
                if k not in excludeKeys:
                    text[k], messages = cls.replaceControlCharacters(
                        text[k],
                        excludeKeys=excludeKeys,
                        excludeCharacters=excludeCharacters,
                        mergeMessages=mergeMessages,
                    )
                    if messages:
                        for m in messages:
                            m.unshiftPath(k)
        elif isinstance(text, list):
            for i in range(0, len(text)):
                text[i], messages = cls.replaceControlCharacters(
                    text[i],
                    excludeKeys=excludeKeys,
                    excludeCharacters=excludeCharacters,
                    mergeMessages=mergeMessages,
                )
                if messages:
                    for m in messages:
                        m.unshiftPath(i)
        elif isinstance(text, str):
            for k in Constants._control_character:
                if Constants._control_character[k][1] in excludeCharacters:
                    continue
                l = len(text)
                text = text.replace(Constants._control_character[k][0], "")
                if len(text) != l:
                    if mergeMessages:
                        messages.append(
                            ReplaceMessage("'%s'" % Constants._control_character[k][1])
                        )
                    else:
                        messages.append(
                            ReplaceMessage(
                                "contained special character '%s'"
                                % Constants._control_character[k][1]
                            )
                        )
        elif isinstance(text, float):
            if math.isnan(text):
                text = None
                messages.append(
                    ReplaceMessage(message="contained a float with 'NaN' value")
                )

        if mergeMessages and messages:
            if len(messages) > 1:
                messages = [
                    ReplaceMessage(
                        message="contained special characters "
                        + ", ".join(m.message for m in messages)
                    )
                ]
            else:
                messages = [
                    ReplaceMessage(
                        message="contained special character " + messages[0].message
                    )
                ]
            # for idx in range(0, len(messages)):
            #     msg = messages[idx]
            #     i = msg.index(0)
            #     if i > 0:
            #         m = ".".join(msg[0:i]) + ": " + " ".join(msg[i + 1 :])
            #         messages[idx] = m

        return text, messages

    @classmethod
    def generateID(cls, len=10):
        return "".join(map(lambda r: chr(random.randint(65, 90)), range(len)))


class SerializeableClass(SerializeableContent):
    _planeClass = True
