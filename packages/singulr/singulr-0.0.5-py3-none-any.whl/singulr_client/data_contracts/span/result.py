# Created by msinghal at 12/09/23
from singulr_client.data_contracts.span.content import KeyedContent
from typing import List, Dict, Any

class Result:
    """
    Represents the result of an operation.

    Attributes:
        inputs (List[KeyedContent]): List of input items.
        outputs (List[KeyedContent]): List of output items.
    """
    def __init__(self):
        self.inputs: List[KeyedContent] = []
        self.outputs: List[KeyedContent] = []

    def get_inputs(self) -> List[KeyedContent]:
        """
        Get the list of input items.

        Returns:
            List[KeyedContent]: List of input items.
        """
        return self.inputs

    def set_inputs(self, inputs: List[KeyedContent]) -> None:
        """
        Set the list of input items.

        Args:
            inputs (List[KeyedContent]): List of input items.
        """
        self.inputs = inputs

    def get_outputs(self) -> List[KeyedContent]:
        """
        Get the list of output items.

        Returns:
            List[KeyedContent]: List of output items.
        """
        return self.outputs

    def set_outputs(self, outputs: List[KeyedContent]) -> None:
        """
        Set the list of output items.

        Args:
            outputs (List[KeyedContent]): List of output items.
        """
        self.outputs = outputs

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the result to a dictionary.

        Returns:
            Dict[str, Any]: The result represented as a dictionary.
        """
        result_dict = {
            "inputs": [input_item.to_dict() for input_item in self.inputs],
            "outputs": [output_item.to_dict() for output_item in self.outputs]
        }
        return result_dict
