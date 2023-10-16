""" Defines soil.data()"""
from typing import (
    Any,
    Dict,
    Optional,
    Type,
    TypeVar,
    TypedDict,
    cast,
    overload,
    TypeAlias,
)

from pandas import DataFrame
from numpy import ndarray

from soil.api import get_result, upload_data, get_alias
from soil.data_structure import DataStructure, get_data_structure_name_and_serialize
from soil import errors
from soil.types import SerializableDataStructure


_GenericDataStructure = TypeVar(
    "_GenericDataStructure", bound=SerializableDataStructure
)
_TypedDict = TypeVar("_TypedDict", bound=TypedDict)
_DataObject: TypeAlias = dict | list | ndarray | DataFrame | _TypedDict


@overload
def data(
    data_object: str,
    metadata: None = None,
    *,
    return_type: None = None,
) -> DataStructure:
    ...


@overload
def data(
    data_object: str,
    metadata: None = None,
    *,
    return_type: Type[_GenericDataStructure],
) -> _GenericDataStructure:
    ...


@overload
def data(
    data_object: _DataObject,
    metadata: dict[str, Any] | None = None,
    *,
    return_type: None = None,
) -> DataStructure:
    ...


@overload
def data(
    data_object: _DataObject,
    metadata: dict[str, Any] | None = None,
    *,
    return_type: Type[_GenericDataStructure],
) -> _GenericDataStructure:
    ...


def data(
    data_object: str | _DataObject,
    metadata: dict[str, Any] | None = None,
    *,
    return_type: Type[_GenericDataStructure] | None = None,
) -> _GenericDataStructure | DataStructure:
    """Load data from the cloud or mark it as uploadable"""
    cast_return_type = DataStructure if return_type is None else return_type
    if isinstance(data_object, str):
        # Data object is an id or an alias
        try:
            data_object = _load_data_alias(data_object)
        except errors.DataNotFound:
            pass
        return cast(cast_return_type, _load_data_id(data_object))  # pyright: ignore
    return cast(
        cast_return_type, _upload_data(data_object, metadata)  # pyright: ignore
    )


def _upload_data(
    data_object: Any, metadata: Optional[Dict[str, Any]] = None
) -> DataStructure:
    ds_name, serialized = get_data_structure_name_and_serialize(data_object)
    result = upload_data(ds_name, serialized, metadata)
    ds = DataStructure(result["_id"], dstype=result["type"])
    return ds


def _load_datastructure(did: str, dtype: str) -> DataStructure:
    # TODO: dynamically load a data structure
    return DataStructure(did, dstype=dtype)


def _load_data_alias(alias: str) -> str:
    return get_alias(alias)["state"]["result_id"]


def _load_data_id(data_id: str) -> DataStructure:
    result = get_result(data_id)
    return _load_datastructure(result["_id"], result["type"])
