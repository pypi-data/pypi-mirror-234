"""
This client can handle three possible request models:
  1.  A direct passthrough of the request object to the GQL server without modification, for example: (id: "abc")
  2.  A nested, or wrapped, request object inside a mapping, for example: (params: {id: "abc"})
  2.a.  The client dynamically assigns the `params` key
  2.b.  The caller defines the static `params` key
This module provides tooling for wrapping requests.
If the caller desires a direct passthrough of the request object, this module should not be used.
"""
from abc import ABC
from dataclasses import dataclass, is_dataclass


@dataclass
class AbstractWrap(ABC):
    """
    Abstract dataclass for nested request params.
    """
    request_params: object | None

    def __new__(cls, *args, **kwargs):
        if cls == AbstractWrap:
            raise TypeError("AbstractWrap cannot be instantiated because it is an abstract class")
        return super().__new__(cls)

    def __init__(self, request_params: object):
        if request_params is not None and not is_dataclass(request_params):
            raise TypeError(f"'request_params' must be a dataclass. Found: {type(request_params)}")
        self.request_params = request_params


@dataclass
class DynamicWrap(AbstractWrap):
    """
    Concrete dataclass for nested request params with a dynamic param name.
    """
    pass

    def __init__(self, request_params: object):
        super().__init__(request_params=request_params)


@dataclass
class StaticWrap(AbstractWrap):
    """
    Concrete dataclass for nested request params with a static param name.
    """
    param_name: str

    def __init__(self, request_params: object, param_name: str):
        super().__init__(request_params=request_params)
        self.param_name = param_name


def wrap_request(
        request_params: object | None = None,
        *,
        param_name: str = None,
) -> DynamicWrap | StaticWrap:
    """
    Return a nested, or wrapped, request object.
    :param request_params: An instance of a dataclass to be nested.
    :param param_name: Optional.  If provided, this will be the mapping key.
    Otherwise the mapping key will be dynamically generated at a later point.
    :return: A nested dataclass with `request_params` matching the input.
    If `param_name` was provided, the returned dataclass will have a `param_name` field matching the input.
    """
    if request_params is not None:
        if not is_dataclass(request_params):
            raise TypeError(f"'request_params' must be a dataclass. Found: {type(request_params)}")
        if isinstance(request_params, type):
            raise TypeError("The dataclass for 'request_params' must be instantiated")

    if isinstance(param_name, str):
        return StaticWrap(request_params=request_params, param_name=param_name)
    return DynamicWrap(request_params=request_params)


def dynamic_mutation_param_wrapper(mutation_name: str) -> str:
    """
    Server side convention for DKIST:
     - create mutations wrap request params with `createParams`
     - update mutations wrap request params with `updateParams`
     - delete mutations wrap request params with `deleteParams`
    """
    if not mutation_name:
        raise ValueError(f"Unable to determine param_wrapper")

    # this works because update, create and delete are all 6 characters
    return f"{mutation_name[:6]}Params"


def dynamic_query_param_wrapper() -> str:
    """
    Server side convention for DKIST:
     - retrieval queries wrap request params with `filterParams`
    """
    return "filterParams"
