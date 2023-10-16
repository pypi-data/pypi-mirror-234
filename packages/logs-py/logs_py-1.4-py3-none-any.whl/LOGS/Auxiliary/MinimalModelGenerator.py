from typing import TYPE_CHECKING, Any, List, Optional, Type, TypeVar, Union, cast

from LOGS.Auxiliary.Constants import Constants
from LOGS.Auxiliary.Tools import Tools

if TYPE_CHECKING:
    from LOGS.LOGSConnection import LOGSConnection

# from LOGS.Entities.SampleMinimal import SampleMinimal


def _typeByTypename(fieldType):
    switcher = {
        "AutoloadSourceMinimal": AutoloadSourceMinimalFromDict,
        "AutoloadSource": AutoloadSourceMinimalFromDict,
        "DatasetMinimal": DatasetMinimalFromDict,
        "Dataset": DatasetMinimalFromDict,
        "EquipmentMinimal": EquipmentMinimalFromDict,
        "Equipment": EquipmentMinimalFromDict,
        "ExperimentMinimal": ExperimentMinimalFromDict,
        "Experiment": ExperimentMinimalFromDict,
        "InstrumentMinimal": InstrumentMinimalFromDict,
        "Instrument": InstrumentMinimalFromDict,
        "MethodMinimal": MethodMinimalFromDict,
        "Method": MethodMinimalFromDict,
        "PersonMinimal": PersonMinimalFromDict,
        "Person": PersonMinimalFromDict,
        "ProjectMinimal": ProjectMinimalFromDict,
        "Project": ProjectMinimalFromDict,
        "SampleMinimal": SampleMinimalFromDict,
        "Sample": SampleMinimalFromDict,
        "LabNotebookEntry": LabNotebookEntryMinimalFromDict,
        "LabNotebookEntryMinimal": LabNotebookEntryMinimalFromDict,
        "Origin": OriginMinimalFromDict,
        "OriginMinimal": OriginMinimalFromDict,
        "InstrumentFacility": InstrumentMinimalFromDict,
        "InstrumentFacilityMinimal": InstrumentMinimalFromDict,
        "Format": FormatMinimalFromDict,
        "FormatMinimal": FormatMinimalFromDict,
        "FormatVendor": FormatVendorMinimalFromDict,
        "FormatVendorMinimal": FormatVendorMinimalFromDict,
        "FormatMethod": FormatMethodMinimalFromDict,
        "FormatMethodMinimal": FormatMethodMinimalFromDict,
        "FormatInstrument": FormatInstrumentMinimalFromDict,
        "FormatInstrumentMinimal": FormatInstrumentMinimalFromDict,
        "FormatFormat": FormatFormatMinimalFromDict,
        "FormatFormatMinimal": FormatFormatMinimalFromDict,
    }
    return switcher.get(fieldType, lambda ref: None)


def MinimalFromSingle(
    value: Any,
    fieldType: str,
    fieldName: Optional[str] = None,
    connection: Optional["LOGSConnection"] = None,
) -> Any:
    from LOGS.Entity.ConnectedEntity import ConnectedEntity

    result = cast(
        Any,
        Tools.checkAndConvert(
            value,
            fieldType=str,
            fieldName=fieldName,
            converter=_typeByTypename(fieldType),
            allowNone=True,
        ),
    )

    if connection:
        if isinstance(result, ConnectedEntity):
            result.connection = connection

    return result


def MinimalFromList(
    value: Any,
    fieldType: str,
    fieldName: Optional[str] = None,
    connection: Optional["LOGSConnection"] = None,
) -> Any:
    from LOGS.Entity.ConnectedEntity import ConnectedEntity

    if isinstance(value, (int, str)):
        value = {"id": value}

    if isinstance(value, list):
        value = [({"id": value} if isinstance(value, (int, str)) else v) for v in value]

    l = Tools.checkListAndConvert(
        value,
        fieldType=str,
        fieldName=fieldName,
        converter=_typeByTypename(fieldType),
        allowNone=True,
    )
    result = list([a for a in l if a])

    if connection:
        for f in result:
            if isinstance(f, ConnectedEntity):
                f.connection = connection

    if len(result) < 1:
        return None

    return result


_T = TypeVar("_T")


def _checkAndConvert(
    value: Any,
    fieldType: Union[Type[_T], List[Type[_T]]],
    fieldName: Optional[str] = None,
    allowNone=False,
    connection: Optional["LOGSConnection"] = None,
) -> _T:
    from LOGS.Entity.ConnectedEntity import ConnectedEntity

    if isinstance(value, (int, str)):
        value = {"id": value}

    result = Tools.checkAndConvert(
        value, fieldType=fieldType, fieldName=fieldName, allowNone=allowNone
    )

    if connection:
        if isinstance(result, ConnectedEntity):
            result.connection = connection

    return result


def AutoloadSourceMinimalFromDict(
    ref: Optional[Union[dict, Constants.ID_TYPE]],
    fieldName: Optional[str] = None,
    connection: Optional["LOGSConnection"] = None,
):
    from LOGS.Entities.AutoloadSourceMinimal import AutoloadSourceMinimal

    return _checkAndConvert(
        ref,
        AutoloadSourceMinimal,
        fieldName=fieldName,
        allowNone=True,
        connection=connection,
    )


def DatasetMinimalFromDict(
    ref: Optional[Union[dict, Constants.ID_TYPE]],
    fieldName: Optional[str] = None,
    connection: Optional["LOGSConnection"] = None,
):
    from LOGS.Entities.DatasetMinimal import DatasetMinimal

    return _checkAndConvert(
        ref, DatasetMinimal, fieldName=fieldName, allowNone=True, connection=connection
    )


def EquipmentMinimalFromDict(
    ref: Optional[Union[dict, Constants.ID_TYPE]],
    fieldName: Optional[str] = None,
    connection: Optional["LOGSConnection"] = None,
):
    from LOGS.Entities.EquipmentMinimal import EquipmentMinimal

    return _checkAndConvert(
        ref,
        EquipmentMinimal,
        fieldName=fieldName,
        allowNone=True,
        connection=connection,
    )


def ExperimentMinimalFromDict(
    ref: Optional[Union[dict, Constants.ID_TYPE]],
    fieldName: Optional[str] = None,
    connection: Optional["LOGSConnection"] = None,
):
    from LOGS.Entities.ExperimentMinimal import ExperimentMinimal

    return _checkAndConvert(
        ref,
        ExperimentMinimal,
        fieldName=fieldName,
        allowNone=True,
        connection=connection,
    )


def InstrumentMinimalFromDict(
    ref: Optional[Union[dict, Constants.ID_TYPE]],
    fieldName: Optional[str] = None,
    connection: Optional["LOGSConnection"] = None,
):
    from LOGS.Entities.InstrumentMinimal import InstrumentMinimal

    return _checkAndConvert(
        ref,
        InstrumentMinimal,
        fieldName=fieldName,
        allowNone=True,
        connection=connection,
    )


def MethodMinimalFromDict(
    ref: Optional[Union[dict, Constants.ID_TYPE]],
    fieldName: Optional[str] = None,
    connection: Optional["LOGSConnection"] = None,
):
    from LOGS.Entities.MethodMinimal import MethodMinimal

    return _checkAndConvert(
        ref, MethodMinimal, fieldName=fieldName, allowNone=True, connection=connection
    )


def PersonMinimalFromDict(
    ref: Optional[Union[dict, Constants.ID_TYPE]],
    fieldName: Optional[str] = None,
    connection: Optional["LOGSConnection"] = None,
):
    from LOGS.Entities.PersonMinimal import PersonMinimal

    return _checkAndConvert(
        ref, PersonMinimal, fieldName=fieldName, allowNone=True, connection=connection
    )


def ProjectMinimalFromDict(
    ref: Optional[Union[dict, Constants.ID_TYPE]],
    fieldName: Optional[str] = None,
    connection: Optional["LOGSConnection"] = None,
):
    from LOGS.Entities.ProjectMinimal import ProjectMinimal

    return _checkAndConvert(
        ref, ProjectMinimal, fieldName=fieldName, allowNone=True, connection=connection
    )


def SampleMinimalFromDict(
    ref: Optional[Union[dict, Constants.ID_TYPE]],
    fieldName: Optional[str] = None,
    connection: Optional["LOGSConnection"] = None,
):
    from LOGS.Entities.SampleMinimal import SampleMinimal

    return _checkAndConvert(
        ref, SampleMinimal, fieldName=fieldName, allowNone=True, connection=connection
    )


def DatasetTypeMinimalFromDict(
    ref: Optional[Union[dict, Constants.ID_TYPE]],
    fieldName: Optional[str] = None,
    connection: Optional["LOGSConnection"] = None,
):
    from LOGS.Entities.DatasetTypeMinimal import DatasetTypeMinimal

    return _checkAndConvert(
        ref,
        DatasetTypeMinimal,
        fieldName=fieldName,
        allowNone=True,
        connection=connection,
    )


def SampleTypeMinimalFromDict(
    ref: Optional[Union[dict, Constants.ID_TYPE]],
    fieldName: Optional[str] = None,
    connection: Optional["LOGSConnection"] = None,
):
    from LOGS.Entities.SampleTypeMinimal import SampleTypeMinimal

    return _checkAndConvert(
        ref,
        SampleTypeMinimal,
        fieldName=fieldName,
        allowNone=True,
        connection=connection,
    )


def LabNotebookEntryMinimalFromDict(
    ref: Optional[Union[dict, Constants.ID_TYPE]],
    fieldName: Optional[str] = None,
    connection: Optional["LOGSConnection"] = None,
):
    from LOGS.Entities.LabNotebookEntryMinimal import LabNotebookEntryMinimal

    return _checkAndConvert(
        ref,
        LabNotebookEntryMinimal,
        fieldName=fieldName,
        allowNone=True,
        connection=connection,
    )


def OriginMinimalFromDict(
    ref: Optional[Union[dict, Constants.ID_TYPE]],
    fieldName: Optional[str] = None,
    connection: Optional["LOGSConnection"] = None,
):
    from LOGS.Entities.OriginMinimal import OriginMinimal

    return _checkAndConvert(
        ref, OriginMinimal, fieldName=fieldName, allowNone=True, connection=connection
    )


def FormatMinimalFromDict(
    ref: Optional[Union[dict, Constants.ID_TYPE]],
    fieldName: Optional[str] = None,
    connection: Optional["LOGSConnection"] = None,
):
    from LOGS.Entities.FormatMinimal import FormatMinimal

    return _checkAndConvert(
        ref, FormatMinimal, fieldName=fieldName, allowNone=True, connection=connection
    )


def FormatVendorMinimalFromDict(
    ref: Optional[Union[dict, Constants.ID_TYPE]],
    fieldName: Optional[str] = None,
    connection: Optional["LOGSConnection"] = None,
):
    from LOGS.Entities.FormatVendorMinimal import FormatVendorMinimal

    return _checkAndConvert(
        ref,
        FormatVendorMinimal,
        fieldName=fieldName,
        allowNone=True,
        connection=connection,
    )


def FormatMethodMinimalFromDict(
    ref: Optional[Union[dict, Constants.ID_TYPE]],
    fieldName: Optional[str] = None,
    connection: Optional["LOGSConnection"] = None,
):
    from LOGS.Entities.FormatMethodMinimal import FormatMethodMinimal

    return _checkAndConvert(
        ref,
        FormatMethodMinimal,
        fieldName=fieldName,
        allowNone=True,
        connection=connection,
    )


def FormatInstrumentMinimalFromDict(
    ref: Optional[Union[dict, Constants.ID_TYPE]],
    fieldName: Optional[str] = None,
    connection: Optional["LOGSConnection"] = None,
):
    from LOGS.Entities.FormatInstrumentMinimal import FormatInstrumentMinimal

    return _checkAndConvert(
        ref,
        FormatInstrumentMinimal,
        fieldName=fieldName,
        allowNone=True,
        connection=connection,
    )


def FormatFormatMinimalFromDict(
    ref: Optional[Union[dict, Constants.ID_TYPE]],
    fieldName: Optional[str] = None,
    connection: Optional["LOGSConnection"] = None,
):
    from LOGS.Entities.FormatFormatMinimal import FormatFormatMinimal

    return _checkAndConvert(
        ref,
        FormatFormatMinimal,
        fieldName=fieldName,
        allowNone=True,
        connection=connection,
    )
