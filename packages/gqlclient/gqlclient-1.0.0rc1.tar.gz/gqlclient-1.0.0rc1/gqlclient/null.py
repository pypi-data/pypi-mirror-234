"""
Define NULL which can be passed as a request argument.
"""
# The inspiration for NULL was drawn from UNSET in the strawberry library.
# The intrepid developer will find striking code similarities between NULL and UNSET.
# NULL and UNSET serve inverse purposes.
from typing import Any
from typing import Optional
from typing import Type


class NullType:
    __instance: Optional["NullType"] = None

    def __new__(cls: Type["NullType"], *args, **kwargs) -> "NullType":
        """singleton"""
        if cls.__instance is None:
            ret = super().__new__(cls)
            cls.__instance = ret
            return ret
        else:
            return cls.__instance

    def __str__(self) -> str:
        """Returns 'null' which is needed for json serialization"""
        return "null"

    def __repr__(self) -> str:
        return "NULL"

    def __bool__(self) -> bool:
        return False

    @classmethod
    def __get_pydantic_core_schema__(
        cls, source_type: "NullType", handler
    ):
        """
        This validator is required to support pydantic V2 dataclass validation.
        This validator roughly equates to: `isinstance(input_value, NullType)` with attendant fluff.
        Since pydantic V2 may not be in use, no pydantic V2 imports can occur until this method gets called.
        The handler, provided by the V2 framework, is a pydantic.GetCoreSchemaHandler.
        The method returns a pydantic_core.CoreSchema to the pydantic V2 framework.
        """
        if source_type is not NullType:
            raise ValueError("This validation is only for NullType")

        # pydantic V2 imports
        # noinspection PyUnresolvedReferences
        from pydantic_core import core_schema
        # noinspection PyUnresolvedReferences
        from pydantic_core import PydanticCustomError
        # noinspection PyUnresolvedReferences
        from pydantic_core.core_schema import ValidationInfo

        def is_null_type(v: Any, info: ValidationInfo) -> Any:
            # Separate validation for json is possible if a need is identified
            if info.mode == "python":
                if not isinstance(v, NullType):
                    raise PydanticCustomError("not_null", "Input must be NULL")
            return v

        null_schema = core_schema.is_instance_schema(cls)
        return core_schema.general_before_validator_function(is_null_type, null_schema)

    @classmethod
    def __get_validators__(cls):
        """
        This validator is required to support pydantic V1 dataclass validation.
        This validator roughly equates to: `isinstance(input_value, NullType)` with attendant fluff.
        Since pydantic V1 may not be in use, no pydantic V1 imports can occur until this method gets called.
        The method returns a validator to the pydantic V1 framework.
        """
        # pydantic V1 imports
        # noinspection PyUnresolvedReferences
        from pydantic.fields import ModelField

        def is_null_type(value, values: dict, config: type, field: ModelField) -> Any:
            if field.type_ is not NullType:
                raise ValueError("This validation is only for NullType")

            if not isinstance(value, NullType):
                raise ValueError("value must be NULL")
            return value

        yield is_null_type


NULL: Any = NullType()

__all__ = [
    "NULL",
]
