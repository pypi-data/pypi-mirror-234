# Created by msinghal at 12/09/23
from typing import Optional
from singulr_client.data_contracts.span.primitive_attribute import BaseAttribute, AttributeType


class LLMInvocationParams(BaseAttribute):
    """
    Represents parameters for LLM (Language Model) invocation.

    Attributes:
        INVOCATION_PARAMETERS (str): The key for invocation parameters.
    """

    INVOCATION_PARAMETERS = "invocation_parameters"

    def __init__(self):
        self.subType: str = ""
        self.model: str = ""
        self.modelName: str = ""
        self.requestTimeOutMillis: int = 0
        self.maxRetries: int = 0
        self.maxTokens: Optional[int] = None
        self.stream: bool = False
        self.temperature: float = 0.0

    def get_key(self) -> str:
        """
        Get the key associated with the invocation parameters.

        Returns:
            str: The key for invocation parameters.
        """
        return self.INVOCATION_PARAMETERS

    def get_type(self):
        return AttributeType.LLM_INVOCATION

    def set_key(self, key: str):
        pass

    def set_type(self, type_):
        pass

    def get_sub_type(self) -> str:
        return self.subType

    def set_sub_type(self, subType: str):
        self.subType = subType

    def get_model(self) -> str:
        return self.model

    def set_model(self, model: str):
        self.model = model

    def get_model_name(self) -> str:
        return self.modelName

    def set_model_name(self, modelName: str):
        self.modelName = modelName

    def get_request_time_out_millis(self) -> int:
        return self.requestTimeOutMillis

    def set_request_time_out_millis(self, requestTimeOutMillis: int):
        self.requestTimeOutMillis = requestTimeOutMillis

    def get_max_retries(self) -> int:
        return self.maxRetries

    def set_max_retries(self, maxRetries: int):
        self.maxRetries = maxRetries

    def get_max_tokens(self) -> Optional[int]:
        return self.maxTokens

    def set_max_tokens(self, maxTokens: Optional[int]):
        self.maxTokens = maxTokens

    def is_stream(self) -> bool:
        return self.stream

    def set_stream(self, stream: bool):
        self.stream = stream

    def get_temperature(self) -> float:
        return self.temperature

    def set_temperature(self, temperature: float):
        self.temperature = temperature
