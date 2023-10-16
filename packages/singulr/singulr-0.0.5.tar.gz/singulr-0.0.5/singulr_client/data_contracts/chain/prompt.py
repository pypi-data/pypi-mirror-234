# Created by msinghal at 12/09/23
from singulr_client.data_contracts.span.primitive_attribute import BaseAttribute, AttributeType
from typing import List


class Prompt(BaseAttribute):
    PROMPT = "prompt"

    def __init__(self):
        self.subType: str = ""
        self.template: str = ""
        self.inputVariables: List[str] = []
        self.templateFormat: str = ""
        self.type: str = self.get_type()

    def get_key(self) -> str:
        return self.PROMPT

    def get_type(self):
        return AttributeType.PROMPT_TEMPLATE

    # Empty methods for serialization and deserialization
    def set_key(self, key: str):
        pass

    def set_type(self, type_):
        pass

    def get_sub_type(self) -> str:
        return self.subType

    def set_sub_type(self, subType: str):
        self.subType = subType

    def get_template(self) -> str:
        return self.template

    def set_template(self, template: str):
        self.template = template

    def get_input_variables(self) -> List[str]:
        return self.inputVariables

    def set_input_variables(self, inputVariables: List[str]):
        self.inputVariables = inputVariables

    def get_template_format(self) -> str:
        return self.templateFormat

    def set_template_format(self, templateFormat: str):
        self.templateFormat = templateFormat
