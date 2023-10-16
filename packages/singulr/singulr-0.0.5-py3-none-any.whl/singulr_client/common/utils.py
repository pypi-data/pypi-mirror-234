# Created by msinghal at 12/09/23
import platform  # Module for platform information
import os
import socket
import psutil  # Modules for OS, networking, and process information
from functools import lru_cache  # Importing LRU cache decorator
import json
import hashlib
import time
from typing import Any, List, Dict

from langchain.callbacks.tracers.schemas import Run

def _hash_id(s: str) -> str:
    """
    Compute an MD5 hash of a string and return the first 16 characters of the hash.

    Args:
        s (str): The input string to be hashed.

    Returns:
        str: The first 16 characters of the MD5 hash of the input string.
    """
    return hashlib.md5(s.encode("utf-8")).hexdigest()[:16]

def _serialize_io(run_inputs: Dict[str, Any]) -> Dict[str, Any]:
    """
    Serialize input data into a dictionary.

    Args:
        run_inputs (dict): A dictionary containing input data.

    Returns:
        dict: A serialized dictionary containing the input data.
    """
    from google.protobuf.json_format import MessageToJson
    from google.protobuf.message import Message

    serialized_inputs = {}
    for key, value in run_inputs.items():
        if isinstance(value, Message):
            serialized_inputs[key] = MessageToJson(value)
        elif key == "input_documents":
            serialized_inputs.update(
                {f"input_document_{i}": json.dumps(doc) for i, doc in enumerate(value)}
            )
        else:
            serialized_inputs[key] = value
    return serialized_inputs

def _fallback_serialize(obj: Any) -> str:
    """
    Serialize a non-serializable object to a string.

    Args:
        obj (Any): The object to be serialized.

    Returns:
        str: A string representation of the object.
    """
    try:
        return f"<<non-serializable: {type(obj).__qualname__}>>"
    except Exception:
        return "<<non-serializable>>"

def _safe_serialize(obj: Dict[str, Any]) -> str:
    """
    Safely serialize a dictionary to a JSON string.

    Args:
        obj (dict): The dictionary to be serialized.

    Returns:
        str: A JSON string representation of the dictionary.
    """
    try:
        return json.dumps(
            obj,
            skipkeys=True,
            default=_fallback_serialize,
        )
    except Exception:
        return "{}"

class CustomEncoder(json.JSONEncoder):
    def default(self, obj):
        if hasattr(obj, 'to_dict') and callable(obj.to_dict):
            return obj.to_dict()
        elif isinstance(obj, list):
            return [self.default(item) for item in obj]
        return super().default(obj)

def generate_trace_id(run: Run) -> str:
    """
    Generate a trace ID based on the Run object and a timestamp.

    Args:
        run (Run): The Run object to be used for generating the trace ID.

    Returns:
        str: The generated trace ID as a string.
    """
    json_str = _safe_serialize(run)
    timestamp = str(time.time())  # Add a timestamp (current time) to the input string
    input_str = json_str + timestamp
    return _hash_id(input_str)
