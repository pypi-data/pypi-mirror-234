# Created by msinghal at 12/09/23
import abc
from enum import Enum
from typing import Type, Dict, Any

from typing_extensions import TypedDict
import attr

from pydantic import BaseModel


class AttributeType(str, Enum):
    """
    Enum representing attribute types.
    """
    UNKNOWN = "UNKNOWN"
    PRIMITIVE_STRING = "PRIMITIVE_STRING"
    PRIMITIVE_INT = "PRIMITIVE_INT"
    LLM_INVOCATION = "LLM_INVOCATION"
    PROMPT_TEMPLATE = "PROMPT_TEMPLATE"
    LLM_STATS = "LLM_STATS"

    def __str__(self) -> str:
        return str(self.value)


class Attribute(metaclass=abc.ABCMeta):
    """
    Base class for attribute objects.
    """
    @abc.abstractmethod
    def get_key(self) -> str:
        """
        Get the key associated with the attribute.

        Returns:
            str: The attribute key.
        """
        pass

    @abc.abstractmethod
    def get_type(self) -> AttributeType:
        """
        Get the attribute type.

        Returns:
            AttributeType: The attribute type.
        """
        pass


class BaseAttribute(Attribute):
    """
    Base class for attribute objects with a key and type.
    """
    def __init__(self, key: str, type: AttributeType):
        self.key = key
        self.type = type

    def get_key(self) -> str:
        return self.key

    def get_type(self) -> AttributeType:
        return self.type

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the attribute to a dictionary.

        Returns:
            Dict[str, Any]: The attribute represented as a dictionary.
        """
        return {
            "key": self.key,
            "type": self.type.value,
        }


class PrimitiveAttribute(BaseAttribute, metaclass=abc.ABCMeta):
    """
    Base class for primitive attribute objects.
    """
    def __init__(self, key: str, type: AttributeType):
        super().__init__(key, type)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "key": self.key,
            "type": self.type.value,
        }


class StringAttribute(PrimitiveAttribute):
    """
    Represents a string attribute.

    Attributes:
        key (str): The unique identifier for the attribute.
        value (str): The string value of the attribute.
    """
    def __init__(self, key: str, value: str):
        super().__init__(key, AttributeType.PRIMITIVE_STRING)
        self.value = value

    def to_json(self) -> Dict[str, Any]:
        return {
            "@type": "string",
            "key": self.key,
            "type": self.type.value,
            "value": self.value
        }

    def to_dict(self) -> Dict[str, Any]:
        return {
            "@type": "str",
            "key": self.key,
            "type": self.type.value,
            "value": self.value
        }


class IntAttribute(PrimitiveAttribute):
    """
    Represents an integer attribute.

    Attributes:
        key (str): The unique identifier for the attribute.
        value (int): The integer value of the attribute.
    """
    def __init__(self, key: str, value: int):
        super().__init__(key, AttributeType.PRIMITIVE_INT)
        self.value = value

    def to_json(self) -> Dict[str, Any]:
        return {
            "@type": "int",
            "key": self.key,
            "type": self.type.value,
            "value": self.value
        }

    def to_dict(self) -> Dict[str, Any]:
        return {
            "@type": "int",
            "key": self.key,
            "type": self.type.value,
            "value": self.value
        }


if __name__ == '__main__':
    s = IntAttribute(key="execution_order", value=1)
    debug = True
