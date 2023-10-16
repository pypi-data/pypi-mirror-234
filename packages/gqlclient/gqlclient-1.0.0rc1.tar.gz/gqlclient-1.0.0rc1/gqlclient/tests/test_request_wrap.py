"""
Tests for request wrapping
"""
from dataclasses import dataclass, asdict

import pytest
from pydantic.dataclasses import dataclass as pydantic_dataclass

from gqlclient.request_wrap import AbstractWrap, DynamicWrap, StaticWrap, wrap_request


@dataclass
class BaseDataclass:
    value: str = "base dataclass"
    optInt: int | None = None


@pydantic_dataclass
class PydDataclass:
    value: str = "pydantic annotated dataclass"
    optInt: int | None = None


@pytest.mark.parametrize(
    "request_params",
    [
        pytest.param(BaseDataclass(), id="base"),
        pytest.param(PydDataclass(), id="pyd"),
        pytest.param(None, id="none"),
    ],
)
def test_dataclasses_dynamic(request_params):
    """ Verify proper dynamic dataclass instantiation """
    result: DynamicWrap = DynamicWrap(request_params=request_params)
    assert result
    assert isinstance(result, DynamicWrap)
    result_data = asdict(result)
    # verify param_name is excluded from result
    assert "param_name" not in result_data.keys()
    assert "request_params" in result_data.keys()
    if request_params is None:
        assert result.request_params is None
    else:
        request_keys_in = asdict(request_params).keys()  # noqa
        request_keys_out = asdict(result.request_params).keys()  # noqa
        assert request_keys_in == request_keys_out


@pytest.mark.parametrize(
    "request_params",
    [
        pytest.param(BaseDataclass(), id="base"),
        pytest.param(PydDataclass(), id="pyd"),
        pytest.param(None, id="none"),
    ],
)
def test_dataclasses_static(request_params):
    """ Verify proper static dataclass instantiation """
    result: StaticWrap = StaticWrap(request_params=request_params, param_name="whatever")
    assert result
    assert isinstance(result, StaticWrap)
    result_data = asdict(result)
    # verify param_name is included in result
    assert "param_name" in result_data.keys()
    assert result_data["param_name"] == "whatever"
    assert "request_params" in result_data.keys()
    if request_params is None:
        assert result.request_params is None
    else:
        request_keys_in = asdict(request_params).keys()  # noqa
        request_keys_out = asdict(result.request_params).keys()  # noqa
        assert request_keys_in == request_keys_out


@pytest.mark.parametrize(
    "request_params, expected_exception_type",
    [
        pytest.param(BaseDataclass(), TypeError, id="base"),
        pytest.param(PydDataclass(), TypeError, id="pyd"),
    ],
)
def test_dataclasses_abstract(request_params, expected_exception_type: type[Exception]):
    """ Verify AbstractWrap cannot be instantiated """
    with pytest.raises(expected_exception_type):
        AbstractWrap(request_params=request_params)


@pytest.mark.parametrize(
    "request_params, expected_exception_type",
    [
        pytest.param("a_string", TypeError, id="string"),
        pytest.param([], TypeError, id="list"),
    ],
)
def test_dataclasses_invalid(request_params, expected_exception_type: type[Exception]):
    """ Verify request params must be a dataclass """
    with pytest.raises(expected_exception_type):
        DynamicWrap(request_params=request_params)
    with pytest.raises(expected_exception_type):
        StaticWrap(request_params=request_params, param_name="whatever")


@pytest.mark.parametrize(
    "request_params",
    [
        pytest.param(BaseDataclass(), id="baseInstance"),
        pytest.param(PydDataclass(), id="pydInstance"),
        pytest.param(None, id="none"),
    ],
)
def test_wrap_request(request_params):
    """ Verify proper result from wrap_request """
    result: DynamicWrap = wrap_request(request_params=request_params)
    assert result
    assert isinstance(result, DynamicWrap)
    result_data = asdict(result)
    # verify param_name is excluded from result
    assert "param_name" not in result_data.keys()
    assert "request_params" in result_data.keys()
    if request_params is None:
        assert result.request_params is None
    else:
        request_keys_in = asdict(request_params).keys()  # noqa
        request_keys_out = asdict(result.request_params).keys()  # noqa
        assert request_keys_in == request_keys_out

    result: StaticWrap = wrap_request(request_params=request_params, param_name="whatever")
    assert result
    assert isinstance(result, StaticWrap)
    result_data = asdict(result)
    # verify param_name is included in result
    assert "param_name" in result_data.keys()
    assert result_data["param_name"] == "whatever"
    assert "request_params" in result_data.keys()
    if request_params is None:
        assert result.request_params is None
    else:
        request_keys_in = asdict(request_params).keys()  # noqa
        request_keys_out = asdict(result.request_params).keys()  # noqa
        assert request_keys_in == request_keys_out


@pytest.mark.parametrize(
    "request_params, expected_exception_type",
    [
        pytest.param("a_string", TypeError, id="string"),
        pytest.param(BaseDataclass, TypeError, id="baseClass"),
        pytest.param(PydDataclass, TypeError, id="pydClass"),
    ],
)
def test_wrap_request_invalid_inputs(request_params, expected_exception_type: type[Exception]):
    """ Verify proper result from wrap_request for invalid input """
    with pytest.raises(expected_exception_type):
        wrap_request(request_params=request_params)
    with pytest.raises(expected_exception_type):
        wrap_request(request_params=request_params, param_name="whatever")
