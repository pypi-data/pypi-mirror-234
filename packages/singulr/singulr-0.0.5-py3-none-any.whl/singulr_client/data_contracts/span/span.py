# Created by msinghal at 12/09/23
from enum import Enum
from typing import List, Optional, Dict, Any
from singulr_client.data_contracts.span.primitive_attribute import PrimitiveAttribute
from singulr_client.data_contracts.span.result import Result

class SpanType(Enum):
    """
    Enumeration representing different types of spans.
    """
    UNKNOWN = "UNKNOWN"
    LLM = "LLM"
    CHAIN = "CHAIN"
    TOOL = "TOOL"
    AGENT = "AGENT"

    def __str__(self) -> str:
        return str(self.value)


class StatusCode(str, Enum):
    """
    Enumeration representing status codes.
    """
    SUCCESS = "SUCCESS"
    ERROR = "ERROR"

    def __str__(self) -> str:
        return str(self.value)


class Span(object):
    """
    Represents a span.

    Args:
        span_id (Optional[str]): The unique identifier of the span.
        name (Optional[str]): The name of the span.
        parent_span_id (Optional[str]): The ID of the parent span.
        trace_id (Optional[str]): The ID of the trace.
        start_time_millis (Optional[int]): The start time of the span in milliseconds.
        end_time_millis (Optional[int]): The end time of the span in milliseconds.
        status_code (Optional[StatusCode]): The status code of the span.
        status_message (Optional[str]): The status message of the span.
        type (Optional[SpanType]): The type of the span.
        sub_type (Optional[str]): The sub-type of the span.
        attributes (Optional[List[PrimitiveAttribute]]): List of attributes associated with the span.
        results (Optional[List[Result]]): List of results associated with the span.
        child_spans (Optional[List["Span"]]): List of child spans.

    Attributes:
        span_id (Optional[str]): The unique identifier of the span.
        name (Optional[str]): The name of the span.
        parent_span_id (Optional[str]): The ID of the parent span.
        trace_id (Optional[str]): The ID of the trace.
        start_time_millis (Optional[int]): The start time of the span in milliseconds.
        end_time_millis (Optional[int]): The end time of the span in milliseconds.
        status_code (Optional[StatusCode]): The status code of the span.
        status_message (Optional[str]): The status message of the span.
        type (Optional[SpanType]): The type of the span.
        sub_type (Optional[str]): The sub-type of the span.
        attributes (List[PrimitiveAttribute]): List of attributes associated with the span.
        results (List[Result]): List of results associated with the span.
        child_spans (List["Span"]): List of child spans.
    """
    def __init__(
        self,
        span_id: Optional[str] = None,
        name: Optional[str] = None,
        parent_span_id: Optional[str] = None,
        trace_id: Optional[str] = None,
        start_time_millis: Optional[int] = None,
        end_time_millis: Optional[int] = None,
        status_code: Optional[StatusCode] = None,
        status_message: Optional[str] = None,
        type: Optional[SpanType] = None,
        sub_type: Optional[str] = None,
        attributes: Optional[List[PrimitiveAttribute]] = None,
        results: Optional[List[Result]] = None,
        child_spans: Optional[List["Span"]] = None,
    ):
        self.span_id = span_id
        self.name = name
        self.parent_span_id = parent_span_id
        self.trace_id = trace_id
        self.start_time_millis = start_time_millis
        self.end_time_millis = end_time_millis
        self.status_code = status_code
        self.status_message = status_message
        self.type = type
        self.sub_type = sub_type
        self.attributes = attributes if attributes is not None else []
        self.results = results if results is not None else []
        self.child_spans = child_spans if child_spans is not None else []

    def add_attribute(self, key: str, value: Any, at_type: str, at_value: str) -> None:
        """
        Add an attribute to the span.

        Args:
            key (str): The key of the attribute.
            value (Any): The value of the attribute.
            at_type (str): The type of the attribute.
            at_value (str): The value of the attribute.
        """
        attr = {
            "@type": at_type,
            "key": key,
            "type": at_value,
            "value": value
        }
        return attr

    def add_named_result(self, inputs: Dict[str, Any], outputs: Dict[str, Any]) -> None:
        """
        Add a named result to the span.

        Args:
            inputs (Dict[str, Any]): The input data.
            outputs (Dict[str, Any]): The output data.
        """
        if self.results is None:
            self.results = []
        self.results.append(Result(inputs, outputs))

    def add_child_span(self, span: "Span") -> None:
        """
        Add a child span to the span.

        Args:
            span (Span): The child span to be added.
        """
        if self.child_spans is None:
            self.child_spans = []
        self.child_spans.append(span)

    def get_span_id(self) -> Optional[str]:
        """
        Get the span ID.

        Returns:
            Optional[str]: The span ID.
        """
        return self.span_id

    def set_span_id(self, span_id: str) -> None:
        """
        Set the span ID.

        Args:
            span_id (str): The span ID.
        """
        self.span_id = span_id

    def get_name(self) -> Optional[str]:
        """
        Get the name of the span.

        Returns:
            Optional[str]: The name of the span.
        """
        return self.name

    def set_name(self, name: str) -> None:
        """
        Set the name of the span.

        Args:
            name (str): The name of the span.
        """
        self.name = name

    # ... (similar methods for other attributes)

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the span to a dictionary.

        Returns:
            Dict[str, Any]: The span represented as a dictionary.
        """
        span_dict = {
            "span_id": self.span_id,
            "name": self.name,
            "parent_span_id": self.parent_span_id,
            "trace_id": self.trace_id,
            "start_time_millis": self.start_time_millis,
            "end_time_millis": self.end_time_millis,
            "status_code": self.status_code.value,
            "status_message": self.status_message,
            "type": self.type.value if self.type else SpanType.UNKNOWN.value,
            "sub_type": self.sub_type,
            "attributes": [attr.to_dict() for attr in self.attributes],
            "results": [result.to_dict() for result in self.results],
            "child_spans": [span.to_dict() for span in self.child_spans],
        }
        # Remove fields with None values
        span_dict = {k: v for k, v in span_dict.items() if v is not None}
        return span_dict
