"""
Tests for NULL processing
"""
from dataclasses import dataclass
from typing import Any

import pytest
from pydantic import ValidationError
from pydantic.dataclasses import dataclass as pydantic_dataclass

from gqlclient.base import GraphQLClientBase
from gqlclient.null import NULL
from gqlclient.null import NullType


@dataclass
class BaseDataclass:
    value: str = "base dataclass"
    optInt: int | None = None
    nullableInt: int | NullType = NULL
    authToken: str = "br549"


@pydantic_dataclass
class PydDataclass:
    value: str = "pydantic annotated dataclass"
    optInt: int | None = None
    nullableInt: int | NullType = NULL
    authToken: str = "br549"


@pytest.mark.parametrize(
    "request_params",
    [
        pytest.param(BaseDataclass(), id="base"),
        pytest.param(PydDataclass(), id="pyd"),
    ],
)
def test_null(request_params: object):
    """
    Verify None fields are excluded from the resulting string.
    Verify authToken field gets excluded from the resulting string.
    Verify NULL field gets retained with a value of `null`.
    """
    result_string = GraphQLClientBase._graphql_query_parameters_from_model(model=request_params)
    assert "value" in result_string
    assert "optInt" not in result_string
    assert "nullableInt" in result_string
    assert "authToken" not in result_string
    for kv_string in result_string.split(","):
        k, v = kv_string.split(":")
        if k.strip() == "nullableInt":
            assert v.strip() == "null"


@pytest.mark.parametrize(
    "request_param",
    [
        pytest.param({"optInt": "a_string"}, id="opt_with_str"),
        pytest.param({"nullableInt": "a_string"}, id="null_with_str"),
        pytest.param({"optInt": NULL}, id="opt_with_null"),
        pytest.param({"nullableInt": None}, id="null_with_none"),
    ],
)
def test_null_invalid(request_param: dict[str, Any]):
    """
    Verify ValidationError for invalid inputs to Pydantic dataclass.
    """
    with pytest.raises(ValidationError):
        PydDataclass(**request_param)
