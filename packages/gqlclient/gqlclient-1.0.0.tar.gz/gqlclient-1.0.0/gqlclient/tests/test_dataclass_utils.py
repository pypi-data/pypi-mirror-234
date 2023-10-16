"""
Test the dataclass_utils
"""
from dataclasses import dataclass
from typing import Any
from typing import ForwardRef
from typing import Optional
from typing import Union

import pytest
from dacite.types import is_optional
from dacite.types import is_union
from pydantic.dataclasses import dataclass as pydantic_dataclass

from gqlclient.dataclass_utils import extract_dataclass
from gqlclient.dataclass_utils import yield_valid_fields

# valid explicit forward references
BaseRef = ForwardRef("BaseDataclass", module=__name__)
PydRef = ForwardRef("PydDataclass", module=__name__)


@dataclass
class BaseWithForwardRef:
    parent_ref: list[BaseRef]
    value: str = "base with forward ref"


@pydantic_dataclass
class PydWithForwardRef:
    parent_ref: list[PydRef]
    value: str = "pydantic annotated with forward ref"


@dataclass
class BaseDataclass:
    child_ref: BaseWithForwardRef
    value: str = "base dataclass"


@pydantic_dataclass
class PydDataclass:
    child_ref: PydWithForwardRef
    value: str = "pydantic annotated dataclass"


@pytest.mark.parametrize(
    "test_type, expected_result",
    [
        pytest.param(Optional[str], True, id="old_opt"),
        pytest.param(Union[str, None], True, id="old_union"),
        pytest.param(str | None, True, id="new_union"),
        pytest.param(str, False, id="str"),
        pytest.param(str | bool, False, id="str_bool"),
        pytest.param(BaseDataclass | bool, False, id="new_base_bool"),
        pytest.param(PydDataclass | bool, False, id="new_pyd_bool"),
        pytest.param(BaseDataclass | None, True, id="new_base_none"),
        pytest.param(PydDataclass | None, True, id="new_pyd_none"),
        pytest.param(Union[BaseDataclass, bool], False, id="old_base_bool"),
        pytest.param(Union[PydDataclass, bool], False, id="old_pyd_bool"),
        pytest.param(Union[BaseDataclass, None], True, id="old_base_none"),
        pytest.param(Union[PydDataclass, None], True, id="old_pyd_none"),
        pytest.param(BaseDataclass | PydDataclass, False, id="new_base_pyd"),
        pytest.param(Union[BaseDataclass, PydDataclass], False, id="old_base_pyd"),
    ],
)
def test_is_optional(test_type: type, expected_result: bool):
    """Verify stability of dacite behavior"""
    assert is_optional(test_type) == expected_result


@pytest.mark.parametrize(
    "test_type, expected_result",
    [
        pytest.param(Optional[str], True, id="old_opt"),
        pytest.param(Union[str, None], True, id="old_union"),
        pytest.param(str | None, True, id="new_union"),
        pytest.param(str, False, id="str"),
        pytest.param(str | bool, True, id="str_bool"),
        pytest.param(BaseDataclass | bool, True, id="new_base_bool"),
        pytest.param(PydDataclass | bool, True, id="new_pyd_bool"),
        pytest.param(BaseDataclass | None, True, id="new_base_none"),
        pytest.param(PydDataclass | None, True, id="new_pyd_none"),
        pytest.param(Union[BaseDataclass, bool], True, id="old_base_bool"),
        pytest.param(Union[PydDataclass, bool], True, id="old_pyd_bool"),
        pytest.param(Union[BaseDataclass, None], True, id="old_base_none"),
        pytest.param(Union[PydDataclass, None], True, id="old_pyd_none"),
        pytest.param(BaseDataclass | PydDataclass, True, id="new_base_pyd"),
        pytest.param(Union[BaseDataclass, PydDataclass], True, id="old_base_pyd"),
    ],
)
def test_is_union(test_type: type, expected_result: bool):
    """Verify stability of dacite behavior"""
    assert is_union(test_type) == expected_result


@pytest.mark.parametrize(
    "test_type, expected_result",
    [
        pytest.param(Optional[str], None, id="old_opt"),
        pytest.param(Union[str, None], None, id="old_union"),
        pytest.param(str | None, None, id="new_union"),
        pytest.param(str, None, id="str"),
        pytest.param(str | bool, None, id="str_bool"),
        pytest.param(BaseDataclass | bool, BaseDataclass, id="new_base_bool"),
        pytest.param(PydDataclass | bool, PydDataclass, id="new_pyd_bool"),
        pytest.param(BaseDataclass | None, BaseDataclass, id="new_base_none"),
        pytest.param(PydDataclass | None, PydDataclass, id="new_pyd_none"),
        pytest.param(Union[BaseDataclass, bool], BaseDataclass, id="old_base_bool"),
        pytest.param(Union[PydDataclass, bool], PydDataclass, id="old_pyd_bool"),
        pytest.param(Union[BaseDataclass, None], BaseDataclass, id="old_base_none"),
        pytest.param(Union[PydDataclass, None], PydDataclass, id="old_pyd_none"),
    ],
)
def test_extract_dataclass_simple(test_type: type, expected_result: Any):
    """Verify proper dataclass extraction"""
    assert extract_dataclass(test_type) == expected_result


@pytest.mark.parametrize(
    "test_type",
    [
        pytest.param(BaseDataclass | PydDataclass, id="new_base_pyd"),
        pytest.param(Union[BaseDataclass, PydDataclass], id="old_base_pyd"),
    ],
)
def test_extract_dataclass_multi(test_type: type):
    """Raise exception when a field has multiple possible dataclasses"""
    with pytest.raises(ValueError):
        extract_dataclass(test_type)


@pytest.mark.parametrize(
    "test_type, expected_result",
    [
        pytest.param(BaseRef, BaseDataclass, id="base"),
        pytest.param(PydRef, PydDataclass, id="pyd"),
        pytest.param(Optional[BaseRef], BaseDataclass, id="opt_base"),
        pytest.param(Optional[PydRef], PydDataclass, id="opt_pyd"),
        pytest.param(Union[BaseRef, None], BaseDataclass, id="union_base"),
        pytest.param(Union[PydRef, None], PydDataclass, id="union_pyd"),
        pytest.param(list[BaseRef], BaseDataclass, id="list_base"),
        pytest.param(list[PydRef], PydDataclass, id="list_pyd"),
        pytest.param(list[Optional[BaseRef]], BaseDataclass, id="list_opt_base"),
        pytest.param(list[Optional[PydRef]], PydDataclass, id="list_opt_pyd"),
        pytest.param(list[Union[BaseRef, bool]], BaseDataclass, id="list_union_base"),
        pytest.param(list[Union[PydRef, bool]], PydDataclass, id="list_union_pyd"),
    ],
)
def test_extract_dataclass_forward_ref_explicit(test_type: type, expected_result: Any):
    """Verify proper dataclass extraction from ForwardRefs"""
    assert extract_dataclass(test_type) == expected_result


@pytest.mark.parametrize(
    "test_type",
    [
        pytest.param(Optional["BaseDataclass"], id="opt_base"),
        pytest.param(Optional["PydDataclass"], id="opt_pyd"),
        pytest.param(Union["BaseDataclass", None], id="union_base"),
        pytest.param(Union["PydDataclass", None], id="union_pyd"),
        pytest.param(list["BaseDataclass"], id="list_base"),
        pytest.param(list["PydDataclass"], id="list_pyd"),
        pytest.param(list[Optional["BaseDataclass"]], id="list_opt_base"),
        pytest.param(list[Optional["PydDataclass"]], id="list_opt_pyd"),
        pytest.param(list[Union["BaseDataclass", bool]], id="list_union_base"),
        pytest.param(list[Union["PydDataclass", bool]], id="list_union_pyd"),
    ],
)
def test_extract_dataclass_forward_ref_implicit(test_type: type):
    """Verify error if an implicit ForwardRef is wrapped by another data type"""
    with pytest.raises(ValueError):
        extract_dataclass(test_type)


@pytest.mark.parametrize(
    "test_type",
    [
        pytest.param(ForwardRef("BaseDataclass"), id="base_none"),
        pytest.param(ForwardRef("PydDataclass"), id="pyd_none"),
        pytest.param(ForwardRef("BaseDataclass", module="abc"), id="base_abc"),
        pytest.param(ForwardRef("PydDataclass", module="abc"), id="pyd_abc"),
    ],
)
def test_extract_dataclass_forward_ref_module(test_type: type):
    """Verify error if ForwardRef has missing or invalid module attribute"""
    with pytest.raises(ValueError):
        extract_dataclass(test_type)


@pytest.mark.parametrize(
    "test_type, test_context, expected_result",
    [
        pytest.param(BaseDataclass, None, {"child_ref", "value"}, id="base_parent_plain"),
        pytest.param(PydDataclass, None, {"child_ref", "value"}, id="pyd_parent_plain"),
        pytest.param(BaseWithForwardRef, None, {"parent_ref", "value"}, id="base_child_plain"),
        pytest.param(PydWithForwardRef, None, {"parent_ref", "value"}, id="pyd_child_plain"),
    ],
)
def test_yield_valid_fields(
    test_type: type,
    test_context: set[str] | str | None,
    expected_result: set[str],
):
    """Verify the fields of the dataclass are returned"""
    fields = {field.name for field in yield_valid_fields(test_type, test_context)}
    assert fields == expected_result


@pytest.mark.parametrize(
    "test_type, test_context, expected_result",
    [
        pytest.param(BaseDataclass, "BaseWithForwardRef", {"value"}, id="base_parent_context"),
        pytest.param(PydDataclass, "PydWithForwardRef", {"value"}, id="pyd_parent_context"),
        pytest.param(BaseWithForwardRef, {"BaseDataclass"}, {"value"}, id="base_child_context"),
        pytest.param(PydWithForwardRef, {"PydDataclass"}, {"value"}, id="pyd_child_context"),
    ],
)
def test_yield_valid_fields_circular(
    test_type: type,
    test_context: set[str] | str | None,
    expected_result: set[str],
):
    """Verify an exception is raised to avoid infinite recursion caused by circular references"""
    with pytest.raises(ValueError):
        fields = {field.name for field in yield_valid_fields(test_type, test_context)}
