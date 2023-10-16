"""
Utilities for working with dataclasses
"""
from dataclasses import Field as dc_field
from dataclasses import fields as dc_fields
from dataclasses import is_dataclass
from types import NoneType
from types import UnionType
from typing import ForwardRef
from typing import Generator
from typing import get_args
from typing import get_origin

from dacite.types import is_optional
from dacite.types import is_union


def extract_dataclass(t: type) -> type | None:
    """
    Extract the dataclass type from a nested dataclass field.
    If no dataclass is found, then None is returned.
    If multiple dataclasses are found, an exception is raised.
    """
    if is_dataclass(t):
        return t

    # eliminate unnecessary downstream processing for NoneType
    if t is NoneType:
        # NoneType is not a dataclass, so return None.
        return None

    # the is_dataclass function does not catch ForwardRefs
    # Also, there is no way to detect a ForwardRef within a list unless the ForwardRef is explicitly declared
    # This is because quoted ForwardRefs within a list come in as a str, rather than a ForwardRef
    if isinstance(t, ForwardRef):
        # get a reference to the specific ForwardRef class from its name and module
        try:
            # noinspection PyUnresolvedReferences
            return t._evaluate(globals(), locals(), frozenset())
        except NameError as ex:
            # A NameError is expected if the ForwardRef module is not defined
            raise ValueError(
                f"Unable to instantiate {t}.  Ensure the ForwardRef module attribute is defined."
            )

    # old style Optional[type] and Union[type, None] are not caught above
    if is_optional(t):
        sub_type = next(iter(get_args(t)))
        # recurse into the sub-type for the Optional
        return extract_dataclass(sub_type)

    # Now deal with compound types
    origin = get_origin(t)

    if origin is None:
        # Not a compound type and already established that t is not a dataclass, so return None.
        return None

    # is_union necessary for old style Union[type1, type2]
    if is_union(t) or issubclass(origin, list | UnionType):
        sub_types = get_args(t)
        if not sub_types:
            raise RuntimeError(f"No args for '{t}' with origin {origin!r}.")
        if any(isinstance(sub_type, str) for sub_type in sub_types):
            raise ValueError(f"Explicit ForwardRef definition required within '{t}'")
        # recursion:  extract the dataclass for each the sub_types
        sub_type_dataclasses = [extract_dataclass(sub_type) for sub_type in sub_types]
        if all(dc is None for dc in sub_type_dataclasses):
            # No dataclasses found in the compound type
            return None
        found_dataclasses = [dc for dc in sub_type_dataclasses if dc is not None]
        if len(found_dataclasses) != 1:
            raise ValueError(f"Unable to reconcile multiple dataclasses of '{t}'")
        return found_dataclasses[0]

    raise RuntimeError(f"Unable to extract dataclass for type '{t}'")


def yield_valid_fields(
    model: type, context: set[str] | str | None = None
) -> Generator[dc_field, None, None]:
    """
    Yield all fields within the dataclass.
    To avoid circular references, an exception is raised if previously visited dataclasses are encountered.
    """
    context = context or set()
    if isinstance(context, str):
        context = {context}

    # noinspection PyDataclass
    for field in dc_fields(model):
        extracted_dataclass = extract_dataclass(field.type)

        # raise an exception if the dataclass has been seen before
        if extracted_dataclass and extracted_dataclass.__name__ in context:
            # prevent infinite loop - raise exception
            raise ValueError(f"Circular Reference in {model.__name__!r} caused by {extracted_dataclass.__name__!r}")

        yield field
