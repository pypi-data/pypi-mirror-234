# Created by msinghal at 12/09/23
import time
from typing import Any, Dict


class PayloadMessage(object):
    """
    Represents a payload message.

    Args:
        id (str): The unique identifier for the message.
        payload (Any): The payload data of the message.
    """

    def __init__(self, id: str, payload: Any):
        self.id = id
        self.source = "source-1"
        self.source_type = "LANG_CHAIN"
        self.timestamp = int(time.time() * 1000)
        self.type = "TRACE"
        self.serialization_type = "JSON"
        self.payload = payload

    def to_dict(self) -> Dict[str, Any]:
        """
        Serialize the PayloadMessage object to a dictionary.

        Returns:
            Dict[str, Any]: A dictionary representation of the object.
        """
        return {
            "id": self.id,
            "source": self.source,
            "source_type": self.source_type,
            "timestamp": self.timestamp,
            "type": self.type,
            "serialization_type": self.serialization_type,
            "payload": self.payload
        }
