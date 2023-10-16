"""
Tests for the Authorization header
"""
from dataclasses import dataclass

import pytest
from pydantic.dataclasses import dataclass as pydantic_dataclass
from requests.structures import CaseInsensitiveDict

from gqlclient.base import GraphQLClientBase

FROM_DATACLASS = "auth_token_from_dataclass"
FROM_HEADER = "auth_token_from_header"


@dataclass
class BaseWithAuthToken:
    value: str = "base dataclass with auth token"
    authToken: str = FROM_DATACLASS


@pydantic_dataclass
class PydWithAuthToken:
    value: str = "pydantic annotated dataclass with auth token"
    authToken: str = FROM_DATACLASS


@dataclass
class BaseWithoutAuthToken:
    value: str = "base dataclass without auth token"


@pydantic_dataclass
class PydWithoutAuthToken:
    value: str = "pydantic annotated dataclass without auth token"


empty_headers = {}
lowercase_auth_header = {"authorization": FROM_HEADER}
uppercase_auth_header = {"Authorization": FROM_HEADER}


@pytest.mark.parametrize(
    "headers_in, request_params, expected_result",
    [
        pytest.param(
            lowercase_auth_header, BaseWithAuthToken(), FROM_HEADER, id="lc_header_with_token_base"
        ),
        pytest.param(
            lowercase_auth_header, PydWithAuthToken(), FROM_HEADER, id="lc_header_with_token_pyd"
        ),
        pytest.param(
            uppercase_auth_header, BaseWithAuthToken(), FROM_HEADER, id="uc_header_with_token_base"
        ),
        pytest.param(
            uppercase_auth_header, PydWithAuthToken(), FROM_HEADER, id="uc_header_with_token_pyd"
        ),
        pytest.param(
            lowercase_auth_header, BaseWithoutAuthToken(), FROM_HEADER, id="lc_header_no_token_base"
        ),
        pytest.param(
            lowercase_auth_header, PydWithoutAuthToken(), FROM_HEADER, id="lc_header_no_token_pyd"
        ),
        pytest.param(
            uppercase_auth_header, BaseWithoutAuthToken(), FROM_HEADER, id="uc_header_no_token_base"
        ),
        pytest.param(
            uppercase_auth_header, PydWithoutAuthToken(), FROM_HEADER, id="uc_header_no_token_pyd"
        ),
    ],
)
def test_authorization_from_header(
    headers_in: dict[str, str], request_params: object, expected_result: str
):
    """
    Verify authorization header is preferred over dataclass authToken.
    Verify authorization header is case agnostic.
    """
    context = {"headers": headers_in}
    GraphQLClientBase._set_auth_header(kwargs=context, mutation_params=request_params)
    headers_out = CaseInsensitiveDict(context.get("headers", {}))
    assert "authorization" in headers_out
    assert headers_out["authorization"] == expected_result


@pytest.mark.parametrize(
    "request_params, expected_result",
    [
        pytest.param(BaseWithAuthToken(), FROM_DATACLASS, id="with_token_base"),
        pytest.param(PydWithAuthToken(), FROM_DATACLASS, id="with_token_pyd"),
    ],
)
def test_authorization_from_dataclass(request_params: object, expected_result: str):
    """
    Verify dataclass authToken is used when no authorization header.
    """
    context = {'headers': {}}
    GraphQLClientBase._set_auth_header(kwargs=context, mutation_params=request_params)
    headers_out = CaseInsensitiveDict(context.get("headers", {}))
    assert "authorization" in headers_out
    assert headers_out["authorization"] == expected_result


@pytest.mark.parametrize(
    "request_params",
    [
        pytest.param(BaseWithoutAuthToken(), id="no_token_base"),
        pytest.param(PydWithoutAuthToken(), id="no_token_pyd"),
    ],
)
def test_authorization_none(request_params: object):
    """
    Verify no change to context if no authToken in dataclass and no authorization header.
    """
    # empty context
    context = {}
    GraphQLClientBase._set_auth_header(kwargs=context, mutation_params=request_params)
    assert not context

    # context with headers dict
    context = {'headers': {}}
    GraphQLClientBase._set_auth_header(kwargs=context, mutation_params=request_params)
    headers_out = CaseInsensitiveDict(context.get("headers", {}))
    assert "authorization" not in headers_out
