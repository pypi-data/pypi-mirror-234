"""
Tests for the graphql_client library
"""

from datetime import datetime
from typing import List
from dataclasses import dataclass

from pydantic.dataclasses import dataclass as pydantic_dataclass
import pytest

from gqlclient import GraphQLClient
from gqlclient.base import dynamic_mutation_param_wrapper
from gqlclient.base import dynamic_query_param_wrapper
from gqlclient.exceptions import ModelException
from gqlclient.request_wrap import StaticWrap, DynamicWrap, AbstractWrap

QUERY_BASE = "query_base"
MUTATION_BASE = "mutation_base"


# Dataclass defined test data
@dataclass
class DataclassRequest:
    str_param: str
    int_param: int
    float_param: float
    str_array_param: List[str]
    num_array_param: List[int]
    bool_param: bool
    date_param: datetime
    optional_param: int = None


@dataclass
class StaticNestedDataclassRequest(StaticWrap):
    request_params: DataclassRequest
    param_name: str = "testParams"


@dataclass
class DynamicNestedDataclassRequest(DynamicWrap):
    request_params: DataclassRequest


@dataclass
class DataclassResponseChild:
    child_param_1: str
    child_param_2: str


@dataclass
class DataclassResponseParent:
    parent_param_1: str
    parent_param_2: str
    child_object: DataclassResponseChild


@dataclass
class DataclassResponseParentWithList:
    parent_param_1: str
    parent_param_2: str
    child_object: List[DataclassResponseChild]


# Pydantic dataclass defined test data
@pydantic_dataclass
class PydanticDataclassRequest:
    str_param: str
    int_param: int
    float_param: float
    str_array_param: List[str]
    num_array_param: List[int]
    bool_param: bool
    date_param: datetime
    optional_param: int = None


@dataclass
class StaticNestedPydanticDataclassRequest(StaticWrap):
    request_params: PydanticDataclassRequest
    param_name: str = "testParams"


@dataclass
class DynamicNestedPydanticDataclassRequest(DynamicWrap):
    request_params: PydanticDataclassRequest


@pydantic_dataclass
class PydanticDataclassResponseChild:
    child_param_1: str
    child_param_2: str


@pydantic_dataclass
class PydanticDataclassResponseParent:
    parent_param_1: str
    parent_param_2: str
    child_object: PydanticDataclassResponseChild


class BadModel:
    def __init__(self):
        self.str_param = ("A",)
        self.int_param = (1,)
        self.float_param = (1.1,)
        self.str_array_param = (["A", "B"],)
        self.num_array_param = ([1, 2],)
        self.date_param = datetime.strptime("2010-03-25T14:08:00", "%Y-%m-%dT%H:%M:%S")


dataclass_request = DataclassRequest(
    str_param="A",
    int_param=1,
    float_param=1.1,
    str_array_param=["A", "B"],
    num_array_param=[1, 2],
    bool_param=False,
    date_param=datetime.strptime("2010-03-25T14:08:00", "%Y-%m-%dT%H:%M:%S"),
)

# static param_name from dataclass definition
static_nested_dataclass_request = StaticNestedDataclassRequest(
    request_params=dataclass_request,
)

dynamic_nested_dataclass_request = DynamicNestedDataclassRequest(
    request_params=dataclass_request,
)

pydantic_dataclass_request = PydanticDataclassRequest(
    str_param="A",
    int_param=1,
    float_param=1.1,
    str_array_param=["A", "B"],
    num_array_param=[1, 2],
    bool_param=False,
    date_param=datetime.strptime("2010-03-25T14:08:00", "%Y-%m-%dT%H:%M:%S"),
)

# static param_name from dataclass definition
static_nested_pydantic_dataclass_request = StaticNestedPydanticDataclassRequest(
    request_params=pydantic_dataclass_request,
)

dynamic_nested_pydantic_dataclass_request = DynamicNestedPydanticDataclassRequest(
    request_params=pydantic_dataclass_request,
)

bad_model = BadModel()


# Graphql Client to test
@pytest.fixture(scope="module")
def client() -> GraphQLClient:
    return GraphQLClient(gql_uri="http://localhost:5000/graphql")


@pytest.mark.parametrize(
    "query_base, request_params, response_cls",
    [
        (QUERY_BASE, dataclass_request, DataclassResponseParent),
        (QUERY_BASE, pydantic_dataclass_request, PydanticDataclassResponseParent),
        (QUERY_BASE, dataclass_request, DataclassResponseParentWithList),
    ],
)
def test_query_passthrough_with_parameters(client, query_base: str, request_params, response_cls):
    """
    Test of query string structure when request params are included for passthrough
    :param client: Graphql Client instance
    :param query_base: Name of the query endpoint
    :param request_params: Instance of a simple dataclass containing the request parameters
    :param response_cls: Dataclass containing the attributes of the graphql response
    :return: None
    """
    assert not isinstance(request_params, AbstractWrap), "Invalid test fixture. Cannot be AbstractWrap for this test."

    test_query = client.get_query(
        query_base=query_base, query_parameters=request_params, query_response_cls=response_cls
    )
    assert "query" in test_query
    expected_query_str = (
        '{query_base('
        'str_param: "A", '
        "int_param: 1, "
        "float_param: 1.1, "
        'str_array_param: ["A", "B"], '
        "num_array_param: [1, 2], "
        "bool_param: false, "
        'date_param: "2010-03-25T14:08:00")'
        "{parent_param_1, parent_param_2, "
        "child_object { child_param_1 child_param_2 }"
        "} }"
    )
    assert test_query["query"] == expected_query_str


@pytest.mark.parametrize(
    "query_base, request_object, response_cls",
    [
        (QUERY_BASE, static_nested_dataclass_request, DataclassResponseParent),
        (QUERY_BASE, static_nested_pydantic_dataclass_request, PydanticDataclassResponseParent),
        (QUERY_BASE, static_nested_dataclass_request, DataclassResponseParentWithList),
    ],
)
def test_query_static_nest_with_parameters(client, query_base: str, request_object, response_cls):
    """
    Test of query string structure when request params and `param_name` are included
    :param client: Graphql Client instance
    :param query_base: Name of the query endpoint
    :param request_object: Instance of a StaticWrap dataclass containing the `request_params` and static `param_name`
    :param response_cls: Dataclass containing the attributes of the graphql response
    :return: None
    """
    assert isinstance(request_object, StaticWrap), "Invalid test fixture. StaticWrap required for this test."

    test_query = client.get_query(
        query_base=query_base, query_parameters=request_object, query_response_cls=response_cls
    )
    param_wrapper = request_object.param_name
    assert "query" in test_query
    expected_query_str = (
        '{query_base('
        f'{param_wrapper}: '
        '{str_param: "A", '
        "int_param: 1, "
        "float_param: 1.1, "
        'str_array_param: ["A", "B"], '
        "num_array_param: [1, 2], "
        "bool_param: false, "
        'date_param: "2010-03-25T14:08:00"})'
        "{parent_param_1, parent_param_2, "
        "child_object { child_param_1 child_param_2 }"
        "} }"
    )
    assert test_query["query"] == expected_query_str


@pytest.mark.parametrize(
    "query_base, request_object, response_cls",
    [
        (QUERY_BASE, dynamic_nested_dataclass_request, DataclassResponseParent),
        (QUERY_BASE, dynamic_nested_pydantic_dataclass_request, PydanticDataclassResponseParent),
        (QUERY_BASE, dynamic_nested_dataclass_request, DataclassResponseParentWithList),
    ],
)
def test_query_dynamic_nest_with_parameters(
        client,
        query_base: str,
        request_object: object,
        response_cls: type,
):
    """
    Test of query string structure when request params are included and `param_name` will be determined dynamically
    :param client: Graphql Client instance
    :param query_base: Name of the query endpoint
    :param request_object: Instance of a DynamicWrap dataclass containing the `request_params`
    :param response_cls: Dataclass containing the attributes of the graphql response
    :return: None
    """
    assert isinstance(request_object, DynamicWrap), "Invalid test fixture. DynamicWrap required for this test."

    test_query = client.get_query(
        query_base=query_base, query_parameters=request_object, query_response_cls=response_cls
    )
    param_wrapper = dynamic_query_param_wrapper()
    assert "query" in test_query
    expected_query_str = (
        '{query_base('
        f'{param_wrapper}: '
        '{str_param: "A", '
        "int_param: 1, "
        "float_param: 1.1, "
        'str_array_param: ["A", "B"], '
        "num_array_param: [1, 2], "
        "bool_param: false, "
        'date_param: "2010-03-25T14:08:00"})'
        "{parent_param_1, parent_param_2, "
        "child_object { child_param_1 child_param_2 }"
        "} }"
    )
    assert test_query["query"] == expected_query_str


@pytest.mark.parametrize(
    "query_base, response_cls",
    [
        (QUERY_BASE, DataclassResponseParent),
        (QUERY_BASE, PydanticDataclassResponseParent)
    ],
)
def test_query_without_parameters(client, query_base: str, response_cls):
    """
    Test of query string structure when parameter model is NOT included
    :param client: Graphql Client instance
    :param query_base: Name of the query endpoint
    :param response_cls: Dataclass containing the attributes of the graphql response
    :return: None
    """
    test_query = client.get_query(query_base=query_base, query_response_cls=response_cls)
    assert "query" in test_query
    expected_query_str = (
        "{query_base"
        "{parent_param_1, parent_param_2, "
        "child_object { child_param_1 child_param_2 }"
        "} }"
    )

    assert test_query["query"] == expected_query_str


@pytest.mark.parametrize(
    "mutation_base, request_params, response_cls",
    [
        (MUTATION_BASE, dataclass_request, DataclassResponseParent),
        (MUTATION_BASE, pydantic_dataclass_request, PydanticDataclassResponseParent),
    ],
)
def test_mutation_passthrough_with_response(client, mutation_base: str, request_params, response_cls):
    """
    Test of mutation string structure when response model is included and request params are included for passthrough
    :param client: Graphql Client instance
    :param mutation_base: Name of the mutation endpoint
    :param request_params: Instance of a simple dataclass containing the request parameters
    :param response_cls: Dataclass containing the attributes of the graphql response
    :return: None
    """
    assert not isinstance(request_params, AbstractWrap), "Invalid test fixture. Cannot be AbstractWrap for this test."

    test_mutation = client.get_mutation(
        mutation_base=mutation_base,
        mutation_response_cls=response_cls,
        mutation_parameters=request_params,
    )
    assert "query" in test_mutation
    assert "operationName" in test_mutation
    expected_query_str = (
        "mutation mutation_base "
        '{mutation_base('
        'str_param: "A", '
        "int_param: 1, "
        "float_param: 1.1, "
        'str_array_param: ["A", "B"], '
        "num_array_param: [1, 2], "
        "bool_param: false, "
        'date_param: "2010-03-25T14:08:00")'
        "{parent_param_1, parent_param_2, child_object "
        "{ child_param_1 child_param_2 }} }"
    )

    assert test_mutation["query"] == expected_query_str
    assert test_mutation["operationName"] == "mutation_base"


@pytest.mark.parametrize(
    "mutation_base, request_object, response_cls",
    [
        (MUTATION_BASE, static_nested_dataclass_request, DataclassResponseParent),
        (MUTATION_BASE, static_nested_pydantic_dataclass_request, PydanticDataclassResponseParent),
    ],
)
def test_mutation_static_nest_with_response(client, mutation_base: str, request_object, response_cls):
    """
    Test of mutation string structure when response model is included and request params and `param_name` are included
    :param client: Graphql Client instance
    :param mutation_base: Name of the mutation endpoint
    :param request_object: Instance of a StaticWrap dataclass containing the `request_params` and static `param_name`
    :param response_cls: Dataclass containing the attributes of the graphql response
    :return: None
    """
    assert isinstance(request_object, StaticWrap), "Invalid test fixture. StaticWrap required for this test."

    test_mutation = client.get_mutation(
        mutation_base=mutation_base,
        mutation_response_cls=response_cls,
        mutation_parameters=request_object,
    )
    param_wrapper = request_object.param_name  # noqa
    assert "query" in test_mutation
    assert "operationName" in test_mutation
    expected_query_str = (
        "mutation mutation_base "
        '{mutation_base('
        f'{param_wrapper}: '
        '{str_param: "A", '
        "int_param: 1, "
        "float_param: 1.1, "
        'str_array_param: ["A", "B"], '
        "num_array_param: [1, 2], "
        "bool_param: false, "
        'date_param: "2010-03-25T14:08:00"})'
        "{parent_param_1, parent_param_2, child_object "
        "{ child_param_1 child_param_2 }} }"
    )

    assert test_mutation["query"] == expected_query_str
    assert test_mutation["operationName"] == "mutation_base"


@pytest.mark.parametrize(
    "mutation_base, request_object, response_cls",
    [
        (MUTATION_BASE, dynamic_nested_dataclass_request, DataclassResponseParent),
        (MUTATION_BASE, dynamic_nested_pydantic_dataclass_request, PydanticDataclassResponseParent),
    ],
)
def test_mutation_dynamic_nest_with_response(client, mutation_base: str, request_object, response_cls):
    """
    Test of mutation string structure when response model is included and request params are included
    and `param_name` will be determined dynamically.
    :param client: Graphql Client instance
    :param mutation_base: Name of the mutation endpoint
    :param request_object: Instance of a DynamicWrap dataclass containing the `request_params`
    :param response_cls: Dataclass containing the attributes of the graphql response
    :return: None
    """
    assert isinstance(request_object, DynamicWrap), "Invalid test fixture. DynamicWrap required for this test."

    test_mutation = client.get_mutation(
        mutation_base=mutation_base,
        mutation_response_cls=response_cls,
        mutation_parameters=request_object,
    )
    param_wrapper = dynamic_mutation_param_wrapper(mutation_base)
    assert "query" in test_mutation
    assert "operationName" in test_mutation
    expected_query_str = (
        "mutation mutation_base "
        '{mutation_base('
        f'{param_wrapper}: '
        '{str_param: "A", '
        "int_param: 1, "
        "float_param: 1.1, "
        'str_array_param: ["A", "B"], '
        "num_array_param: [1, 2], "
        "bool_param: false, "
        'date_param: "2010-03-25T14:08:00"})'
        "{parent_param_1, parent_param_2, child_object "
        "{ child_param_1 child_param_2 }} }"
    )

    assert test_mutation["query"] == expected_query_str
    assert test_mutation["operationName"] == "mutation_base"


@pytest.mark.parametrize(
    "mutation_base, request_params",
    [
        (MUTATION_BASE, dataclass_request),
        (MUTATION_BASE, pydantic_dataclass_request)
    ],
)
def test_mutation_passthrough_without_response(client, mutation_base: str, request_params):
    """
    Test of mutation string structure when response model is NOT included
    and request params are included for passthrough
    :param client: Graphql Client instance
    :param mutation_base: Name of the mutation endpoint
    :param request_params: Instance of a simple dataclass containing the request parameters
    :return: None
    """
    assert not isinstance(request_params, AbstractWrap), "Invalid test fixture. Cannot be AbstractWrap for this test."

    test_mutation = client.get_mutation(mutation_base=mutation_base, mutation_parameters=request_params)
    assert "query" in test_mutation
    assert "operationName" in test_mutation
    expected_query_str = (
        "mutation mutation_base "
        '{mutation_base('
        'str_param: "A", '
        "int_param: 1, float_param: 1.1, "
        'str_array_param: ["A", "B"], '
        "num_array_param: [1, 2], "
        "bool_param: false, "
        'date_param: "2010-03-25T14:08:00") }'
    )

    assert test_mutation["query"] == expected_query_str
    assert test_mutation["operationName"] == "mutation_base"


@pytest.mark.parametrize(
    "mutation_base, request_object",
    [
        (MUTATION_BASE, static_nested_dataclass_request),
        (MUTATION_BASE, static_nested_pydantic_dataclass_request)
    ],
)
def test_mutation_static_nest_without_response(client, mutation_base: str, request_object):
    """
    Test of mutation string structure when response model is NOT included
    but request params and `param_name` are included
    :param client: Graphql Client instance
    :param mutation_base: Name of the mutation endpoint
    :param request_object: Instance of a StaticWrap dataclass containing the `request_params` and static `param_name`
    :return: None
    """
    assert isinstance(request_object, StaticWrap), "Invalid test fixture. StaticWrap required for this test."

    test_mutation = client.get_mutation(mutation_base=mutation_base, mutation_parameters=request_object)
    param_wrapper = request_object.param_name
    assert "query" in test_mutation
    assert "operationName" in test_mutation
    expected_query_str = (
        "mutation mutation_base "
        '{mutation_base('
        f'{param_wrapper}: '
        '{str_param: "A", '
        "int_param: 1, float_param: 1.1, "
        'str_array_param: ["A", "B"], '
        "num_array_param: [1, 2], "
        "bool_param: false, "
        'date_param: "2010-03-25T14:08:00"}) }'
    )

    assert test_mutation["query"] == expected_query_str
    assert test_mutation["operationName"] == "mutation_base"


@pytest.mark.parametrize(
    "mutation_base, request_object",
    [
        (MUTATION_BASE, dynamic_nested_dataclass_request),
        (MUTATION_BASE, dynamic_nested_pydantic_dataclass_request)
    ],
)
def test_mutation_dynamic_nest_without_response(client, mutation_base: str, request_object):
    """
    Test of mutation string structure when response model is NOT included and request params are included
    and `param_name` will be determined dynamically.
    :param client: Graphql Client instance
    :param mutation_base: Name of the mutation endpoint
    :param request_object: Instance of a DynamicWrap dataclass containing the `request_params`
    :return: None
    """
    assert isinstance(request_object, DynamicWrap), "Invalid test fixture. DynamicWrap required for this test."

    test_mutation = client.get_mutation(mutation_base=mutation_base, mutation_parameters=request_object)
    param_wrapper = dynamic_mutation_param_wrapper(mutation_name=mutation_base)
    assert "query" in test_mutation
    assert "operationName" in test_mutation
    expected_query_str = (
        "mutation mutation_base "
        '{mutation_base('
        f'{param_wrapper}: '
        '{str_param: "A", '
        "int_param: 1, float_param: 1.1, "
        'str_array_param: ["A", "B"], '
        "num_array_param: [1, 2], "
        "bool_param: false, "
        'date_param: "2010-03-25T14:08:00"}) }'
    )

    assert test_mutation["query"] == expected_query_str
    assert test_mutation["operationName"] == "mutation_base"


@pytest.mark.parametrize(
    "response_model_cls, parameter_model", [(BadModel, None), (DataclassResponseParent, bad_model)]
)
def test_bad_model(client, response_model_cls, parameter_model):
    """
    Test of a non-dataclass object causing a ValueError
    :param client: Graphql Client instance
    :param response_model_cls: Object representing the graphql response
    :param parameter_model: Object representing the graphql parameters
    :return: None
    """

    with pytest.raises(ModelException):
        client.get_query(QUERY_BASE, response_model_cls, parameter_model)


def test_query_with_empty_parameters(client):
    """
    Test query with a parameter object with all None attribute values
    :param client: Graphql Client instance
    :return:
    """

    empty_dataclass_parameters = DataclassRequest(
        str_param=None,
        int_param=None,
        float_param=None,
        str_array_param=None,
        num_array_param=None,
        bool_param=None,
        date_param=None,
    )

    test_query = client.get_query(
        query_base=QUERY_BASE,
        query_parameters=empty_dataclass_parameters,
        query_response_cls=DataclassResponseParent,
    )
    assert "query" in test_query
    expected_query_str = (
        "{query_base"
        "{parent_param_1, parent_param_2, "
        "child_object { child_param_1 child_param_2 }"
        "} }"
    )

    assert test_query["query"] == expected_query_str


def test_three_layered_response(client):
    @dataclass
    class Grandchild:
        gchild_name: str

    @dataclass
    class Child:
        child_name: str
        grandchild: Grandchild

    @dataclass
    class Parent:
        parent_name: str
        child: Child

    test_query = client.get_query("threeLayerTest", Parent)

    expected_query = {
        "query": "{threeLayerTest"
        "{parent_name, "
        "child { child_name grandchild { gchild_name } }"
        "} }"
    }
    assert test_query == expected_query
