# Created by msinghal at 12/09/23
from singulr_client.data_contracts.span.primitive_attribute import BaseAttribute, AttributeType

class TokenUsage:
    """
    Represents token usage statistics.

    Attributes:
        promptTokens (int): The number of prompt tokens used.
        completionTokens (int): The number of completion tokens used.
        totalTokens (int): The total number of tokens used.
    """

    def __init__(self):
        self.promptTokens: int = 0
        self.completionTokens: int = 0
        self.totalTokens: int = 0

    def get_prompt_tokens(self) -> int:
        """
        Get the number of prompt tokens used.

        Returns:
            int: The number of prompt tokens used.
        """
        return self.promptTokens

    def set_prompt_tokens(self, promptTokens: int):
        """
        Set the number of prompt tokens used.

        Args:
            promptTokens (int): The number of prompt tokens used.
        """
        self.promptTokens = promptTokens

    def get_completion_tokens(self) -> int:
        """
        Get the number of completion tokens used.

        Returns:
            int: The number of completion tokens used.
        """
        return self.completionTokens

    def set_completion_tokens(self, completionTokens: int):
        """
        Set the number of completion tokens used.

        Args:
            completionTokens (int): The number of completion tokens used.
        """
        self.completionTokens = completionTokens

    def get_total_tokens(self) -> int:
        """
        Get the total number of tokens used.

        Returns:
            int: The total number of tokens used.
        """
        return self.totalTokens

    def set_total_tokens(self, totalTokens: int):
        """
        Set the total number of tokens used.

        Args:
            totalTokens (int): The total number of tokens used.
        """
        self.totalTokens = totalTokens

class LLMStats(BaseAttribute):
    """
    Represents Language Model (LLM) statistics.

    Attributes:
        LLM_OUTPUT (str): The key for LLM output.
    """

    LLM_OUTPUT = "llm_output"

    def __init__(self):
        self.subType: str = ""
        self.tokenUsage: TokenUsage = TokenUsage()
        self.modelName: str = ""

    def get_key(self) -> str:
        """
        Get the key associated with LLM output.

        Returns:
            str: The key for LLM output.
        """
        return self.LLM_OUTPUT

    def get_type(self):
        return AttributeType.LLM_STATS

    def set_key(self, key: str):
        pass

    def set_type(self, type_):
        pass

    def get_sub_type(self) -> str:
        return self.subType

    def set_sub_type(self, subType: str):
        """
        Set the subtype of LLM statistics.

        Args:
            subType (str): The subtype of LLM statistics.
        """
        self.subType = subType

    def get_token_usage(self) -> TokenUsage:
        """
        Get the token usage statistics.

        Returns:
            TokenUsage: Token usage statistics.
        """
        return self.tokenUsage

    def set_token_usage(self, tokenUsage: TokenUsage):
        """
        Set the token usage statistics.

        Args:
            tokenUsage (TokenUsage): Token usage statistics.
        """
        self.tokenUsage = tokenUsage

    def get_model_name(self) -> str:
        """
        Get the name of the language model.

        Returns:
            str: The name of the language model.
        """
        return self.modelName

    def set_model_name(self, modelName: str):
        """
        Set the name of the language model.

        Args:
            modelName (str): The name of the language model.
        """
        self.modelName = modelName
