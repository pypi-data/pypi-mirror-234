"""
Base class to support the creation of graphql queries and mutations.
"""
import datetime
import json
import logging
from abc import ABC
from abc import abstractmethod
from dataclasses import asdict
from dataclasses import dataclass
from dataclasses import Field as dc_field
from dataclasses import fields as dc_fields
from dataclasses import is_dataclass
from typing import Any
from typing import Callable

from requests.structures import CaseInsensitiveDict

from gqlclient.dataclass_utils import extract_dataclass
from gqlclient.dataclass_utils import yield_valid_fields
from gqlclient.exceptions import GraphQLException
from gqlclient.exceptions import ModelException
from gqlclient.null import NullType
from gqlclient.request_wrap import AbstractWrap, StaticWrap, dynamic_mutation_param_wrapper, dynamic_query_param_wrapper
from gqlclient.response_encoders import dataclass_encoder

__all__ = ["GraphQLClientBase"]


logger = logging.getLogger(__name__)


class CombinedEncoder(json.JSONEncoder):
    """
    A JSON encoder which encodes datetimes as iso formatted strings.
    """

    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.isoformat("T")
        if isinstance(obj, NullType):
            return None
        return super().default(obj)


@dataclass
class DefaultParameters:
    """
    Default parameter object that will pass dataclass type checking
    """


class GraphQLClientBase(ABC):
    """
    Abstract class for formatting and executing GraphQL queries and mutations

    :param gql_uri: Fully qualified URI for the graphQL endpoint.
    """

    def __init__(
        self,
        gql_uri: str,
        default_response_encoder: Callable[[str, dict, type], Any] | None = dataclass_encoder,
    ):
        """
        Base constructor for the Graphql client
        :param gql_uri: URI for the graphql endpoint
        :param default_response_encoder: Optional default encoder for graphql responses.  e.g. dataclass_encoder
        """
        self.gql_uri = gql_uri
        self.default_response_encoder = default_response_encoder

    @staticmethod
    def _graphql_response_from_model(model_cls: type) -> str:
        """
        Generate a GraphQL Response query from the class for the response.

        :param model_cls: Dataclass type representing the desired response object from the graphql endpoint.

        :return: Portion of a graphql query which specifies the response object.
        """
        if not is_dataclass(model_cls):
            raise ModelException("Response model must be a dataclass")

        def parse_field(field: dc_field, context: set[str]) -> str | tuple[str, list[str]] | None:
            """
            For a simple datatype, return the field name as a str.
            For a dataclass, return a 2-tuple,
             with the first element being the field name
             and the second element being a list of the fields within the dataclass.
            Nested dataclasses will result in recursion.
            """
            extracted_dataclass = extract_dataclass(field.type)

            if not extracted_dataclass:
                return field.name

            # each fork must have its own context to identify circular references specific to the branch
            branch_context = set(context)
            branch_context.add(extracted_dataclass.__name__)
            return (
                field.name,
                [
                    parse_field(sub_field, branch_context)
                    for sub_field in yield_valid_fields(extracted_dataclass, branch_context)
                ],
            )

        def unpack(name: tuple[str, list[str]] | str) -> str:
            if not isinstance(name, tuple):
                return name
            # dataclass name followed by its fields in curly braces
            return f"{name[0]} {{ {' '.join([unpack(n) for n in name[1]])} }}"

        root_context = {model_cls.__name__}
        names = [parse_field(f, root_context) for f in yield_valid_fields(model_cls, root_context)]
        names = [unpack(name) for name in names]
        return ", ".join(names)

    @staticmethod
    def _graphql_query_parameters_from_model(model: object) -> str:
        """
        Generate GraphQL query parameters from the dataclass instance.

        :param model: Dataclass instance with the actual search values

        :return: Portion of a graphql query which specifies the query parameters
        """

        if not is_dataclass(model):
            raise ModelException("Parameter model must be a dataclass")

        # Only create query parameters for those with values using graphql syntax mask for the query parameters
        # noinspection PyDataclass
        parameters = ", ".join(
            [
                f"{field.name}: {json.dumps(getattr(model, field.name), cls=CombinedEncoder)}"
                for field in dc_fields(model)
                if field.name != "authToken" and getattr(model, field.name) is not None
            ]
        )
        return parameters

    # TODO DD - remove this method and references once conversion to Authorization header is complete
    @staticmethod
    def _set_auth_header(kwargs: dict, mutation_params: object):
        """
        Add authorization header to the request kwargs when appropriate.
        This can modify the kwargs that are passed in.

        :param kwargs: Optional arguments for an http request. e.g. headers
        :param mutation_params: A dataclass instance that may include an authToken
        """
        headers_in = kwargs.get("headers")
        if not isinstance(headers_in, dict) and headers_in is not None:
            # if headers is not a dict, return without making any changes to the kwargs
            return

        # header keys are case insensitive
        headers_in = CaseInsensitiveDict(headers_in)
        # Prefer the authorization header, if provided, over authToken from the mutation parameters
        # noinspection PyDataclass
        if "authorization" not in headers_in and (
            auth_token := asdict(mutation_params).get("authToken")
        ):
            # if necessary, add the headers key.  Then set the authorization key within.
            kwargs.setdefault("headers", {})["authorization"] = auth_token

    @staticmethod
    def _get_param_wrapper(
            model: object,
            *,
            mutation_base: str | None = None,
    ) -> tuple[str, object]:
        """
        Return a GraphQL query param name and param values from the provided dataclass instance.

        :param model: Dataclass instance with the actual request parameters
        :param mutation_base: Optional mutation name.  Must be provided for mutations using a dynamic param_name.

        :return: A 2-tuple:  The first element is the `param_name` and the second is a dataclass with the `request` parameters.
        """

        if not is_dataclass(model):
            raise ModelException("Parameter model must be a dataclass")

        if not isinstance(model, AbstractWrap):
            # simply passthrough the request as is
            return "", model

        if model.request_params is None:
            model.request_params = DefaultParameters

        if isinstance(model, StaticWrap):
            # nest the request with the static param name provided
            return model.param_name, model.request_params

        # nest the request with a dynamic param name assigned by this client
        if mutation_base:
            return dynamic_mutation_param_wrapper(mutation_base), model.request_params
        return dynamic_query_param_wrapper(), model.request_params

    def get_query(
        self,
        query_base: str,
        query_response_cls: type,
        query_parameters: object | None = DefaultParameters,
    ) -> dict[str, str]:
        """
        Create a GraphQL formatted query string.

        :param query_base: Name of the root type to be queried
        :param query_response_cls: A dataclass model class representing the structure of the response object
        with attributes corresponding to the Graphql type and attribute names
        :param query_parameters: Optional. Instance of a dataclass model containing attributes corresponding
        to parameter names and values corresponding to the parameter value.

        :return: Dictionary that can be passed as json to the GraphQL API endpoint
        """

        # Construct graphql query
        gql_query = query_base
        param_wrapper, query_parameters = self._get_param_wrapper(query_parameters)
        parameters = self._graphql_query_parameters_from_model(query_parameters)
        if parameters and param_wrapper:
            # resulting format: (params: {id: "abc"})
            gql_query += f"({param_wrapper}: {{{parameters}}})"
        elif parameters:
            # resulting format: (id: "abc")
            gql_query += f"({parameters})"

        gql_query += f"{{{self._graphql_response_from_model(query_response_cls)}}}"
        return {"query": f"{{{gql_query} }}"}

    def get_mutation(
        self,
        mutation_base: str,
        mutation_parameters: object,
        mutation_response_cls: type | None = None,
    ) -> dict[str, str]:
        """
        Create a GraphQL formatted mutation string.

        :param mutation_base: Name of the root type to be mutated
        :param mutation_parameters: Instance of a dataclass model containing attributes corresponding to
        parameter names and values corresponding to the parameter value.
        :param mutation_response_cls: Optional. A dataclass model class representing the structure of the
        response object with attributes corresponding to the Graphql type and attribute names.

        :return: Dictionary that can be passed as json to the GraphQL API endpoint
        """

        # Construct graphql mutation
        gql_mutation = f"mutation {mutation_base} {{{mutation_base}"
        param_wrapper, mutation_parameters = self._get_param_wrapper(mutation_parameters, mutation_base=mutation_base)
        parameters = self._graphql_query_parameters_from_model(mutation_parameters)
        if param_wrapper:
            # resulting format: (params: {id: "abc"})
            gql_mutation += f"({param_wrapper}: {{{parameters}}})"
        else:
            # resulting format: (id: "abc")
            gql_mutation += f"({parameters})"

        if mutation_response_cls:
            gql_mutation += f"{{{self._graphql_response_from_model(mutation_response_cls)}}}"
        gql_mutation += " }"

        return {"query": f"{gql_mutation}", "operationName": mutation_base}

    @abstractmethod
    def execute_gql_call(self, query: dict, **kwargs) -> dict:
        """
        Executes a GraphQL query or mutation.

        :param query: Dictionary formatted graphql query

        :param kwargs: Optional arguments that the http client takes. e.g. headers

        :return: Dictionary containing the response from the GraphQL endpoint
        """

    def _format_response(
        self,
        query_base: str,
        response_cls,
        result: dict,
        response_encoder: Callable[[str, dict, type], Any] | None,
    ):
        """
        Helper function to format the graphql response using a provided encoder
        :param result: Graphql Response to format
        :param response_encoder: Encoder to use in formatting
        :return:
        """
        if response_encoder is None:  # Use the default encoder from the instance
            response_encoder = self.default_response_encoder
        if "errors" in result:
            raise GraphQLException(errors=result["errors"])
        if response_encoder is None:
            return result["data"]  # dict return
        else:
            return response_encoder(query_base, result["data"], response_cls)

    def execute_gql_query(
        self,
        query_base: str,
        query_response_cls: type,
        query_parameters: object | None = DefaultParameters,
        response_encoder: Callable[[str, list[dict] | dict, type], Any] | None = None,
        **kwargs,
    ) -> Any:
        """
        Executes a graphql query based upon input dataclass models.

        :param query_base: Name of the root type to be queried

        :param query_parameters: Optional. Instance of a dataclass model containing attributes corresponding to
        parameter names and values corresponding to the parameter value.

        :param query_response_cls: A dataclass model class representing the structure of the response
        object with attributes corresponding to the Graphql type and attribute names

        :param response_encoder: A callable which takes a dict graphql response and returns a reformatted type

        :param kwargs: Optional arguments that http client (`requests`) takes. e.g. headers


        :return: The response formatted by the specified response_encoder.  Default is dict if no encoder is specified
        """
        query = self.get_query(query_base, query_response_cls, query_parameters)
        result = self.execute_gql_call(query, **kwargs)
        return self._format_response(query_base, query_response_cls, result, response_encoder)

    def execute_gql_mutation(
        self,
        mutation_base: str,
        mutation_parameters: object,
        mutation_response_cls: type | None = None,
        response_encoder: Callable[[str, list[dict] | dict, type], Any] | None = None,
        **kwargs,
    ) -> Any:
        """
        Executes a graphql mutation based upon input dataclass models.

        :param mutation_base: Name of the root type to be mutated

        :param mutation_parameters: Instance of a dataclass model containing attributes corresponding to
        parameter names and values corresponding to the parameter value.

        :param mutation_response_cls: Optional. A dataclass model class representing the structure of the
        response object with attributes corresponding to the Graphql type and attribute names.

        :param response_encoder: A callable which takes the following arguments:
            str for the base type call e.g. query_base or mutation_base
            dict for the data returned in under the 'data' key
            type for the dataclass that structured the response

        :param kwargs: Optional arguments that http client (`requests`) takes. e.g. headers

        :return: The response formatted by the specified response_encoder.  Default is dict if no encoder is specified
        """
        mutation = self.get_mutation(mutation_base, mutation_parameters, mutation_response_cls)
        self._set_auth_header(kwargs, mutation_parameters)
        result = self.execute_gql_call(mutation, **kwargs)
        return self._format_response(mutation_base, mutation_response_cls, result, response_encoder)

    def __str__(self):
        return f"GraphQLClient(gql_uri={self.gql_uri}, default_response_encoder={self.default_response_encoder})"

    def __repr__(self):
        return str(self)
