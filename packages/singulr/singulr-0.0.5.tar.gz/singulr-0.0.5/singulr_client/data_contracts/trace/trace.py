# Created by msinghal at 12/09/23
from typing import Optional, Dict
from singulr_client.data_contracts.env.environment import Environment
from singulr_client.data_contracts.span.span import Span
import json

class TraceTree:
    """
    Represents a trace tree.

    Args:
        trace_id (Optional[str]): The ID of the trace.
        environment (Optional[Environment]): The environment associated with the trace tree.
        root_span (Optional[Span]): The root span of the trace tree.

    Attributes:
        trace_id (Optional[str]): The ID of the trace.
        environment (Optional[Environment]): The environment associated with the trace tree.
        root_span (Optional[Span]): The root span of the trace tree.
    """
    def __init__(self, trace_id: Optional[str] = None, environment: Optional[Environment] = None, root_span: Optional[Span] = None):
        self.trace_id = trace_id if trace_id is not None else self.trace_id
        self.environment = environment if environment is not None else self.environment
        self.root_span = root_span if root_span is not None else self.root_span

    def to_dict(self) -> Dict[str, any]:
        """
        Convert the trace tree to a dictionary.

        Returns:
            Dict[str, any]: The trace tree represented as a dictionary.
        """
        trace_tree_dict = {
            "trace_id": self.trace_id,
            "environment": self.environment.to_dict() if self.environment else None,
            "root_span": self.root_span.to_dict() if self.root_span else None
        }
        # Remove fields with None values
        trace_tree_dict = {k: v for k, v in trace_tree_dict.items() if v is not None}
        return trace_tree_dict

    def to_json(self) -> dict:
        """
        Convert the trace tree to a JSON string.

        Returns:
            dict: The trace tree represented as a JSON string.
        """
        trace_tree_dict = self.to_dict()
        json_string = json.dumps(trace_tree_dict)
        print("trace_tree dict: \n {}".format(trace_tree_dict))
        print("trace_tree json: \n {}".format(json_string))
        return json_string
