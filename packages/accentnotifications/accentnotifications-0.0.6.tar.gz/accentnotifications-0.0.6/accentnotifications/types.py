from email import message_from_bytes, message_from_string
from email.message import Message
from typing import Any, Callable

from pydantic_core import core_schema


class Email(Message):
    @classmethod
    def __get_validators__(cls):
        yield cls._validate

    @classmethod
    def _validate(cls, v) -> Message:
        try:
            if isinstance(v, str):
                return message_from_string(v)
            elif isinstance(v, bytes):
                return message_from_bytes(v)
        except Exception as e:
            raise ValueError("invalid format.") from e

        if not isinstance(v, Message):
            raise ValueError("invalid format.")

        return v

    @classmethod
    def __get_pydantic_core_schema__(
        cls,
        _source_type: Any,
        _handler: Callable[[Any], core_schema.CoreSchema],
    ) -> core_schema.CoreSchema:
        def validate_from_str(value: str) -> Message:
            result = message_from_string(value)
            return result

        from_str_schema = core_schema.chain_schema(
            [
                core_schema.str_schema(),
                core_schema.no_info_plain_validator_function(validate_from_str),
            ]
        )

        return core_schema.json_or_python_schema(
            json_schema=from_str_schema,
            python_schema=core_schema.union_schema(
                [
                    core_schema.is_instance_schema(Message),
                    from_str_schema,
                ]
            ),
            serialization=core_schema.plain_serializer_function_ser_schema(
                lambda instance: instance.as_string()
            ),
        )
