# Created by msinghal at 12/09/23
from enum import Enum
from typing import Optional, Dict, Union

class ContentType(str, Enum):
    """
    Enum representing content types.
    """
    GENERATION = "GENERATION"
    TEXT_DOCUMENT = "TEXT_DOCUMENT"

class DocumentType(Enum):
    """
    Enum representing document types.
    """
    TEXT = "TEXT"
    ADDRESSABLE_CTX_DOCUMENT = "ADDRESSABLE_CTX_DOCUMENT"
class KeyedContent:
    """
    Represents content with a key, content, and content type.

    Attributes:
        key (str): The unique identifier for the content.
        content (str): The content data.
        content_type (ContentType): The content type.
    """

    def __init__(self, key: str, content: str, content_type: ContentType):
        self.key: str = key
        self.content: str = content
        self.content_type: ContentType = content_type

    def __str__(self) -> str:
        return str(self.value)

    def to_json(self) -> dict:
        return self.value

    def to_dict(self) -> Dict[str, Union[str, ContentType]]:
        """
        Convert the content to a dictionary.

        Returns:
            Dict[str, Union[str, ContentType]]: The content represented as a dictionary.
        """
        return {
            "key": self.key,
            "content_type": self.content_type.value,
            "content": self.content
        }

class GenerationDocument(KeyedContent):
    """
    Represents a generation document with additional generation information.

    Attributes:
        key (str): The unique identifier for the content.
        content (str): The content data.
    """

    def __init__(self, key: str, content: str):
        super().__init__(key, content, ContentType.GENERATION)
        self.generation_info: GenerationInfo = GenerationInfo()

    def to_dict(self) -> Dict[str, Union[str, ContentType]]:
        return {
            "@type": "generation_content",
            "key": self.key,
            "content_type": self.content_type.value,
            "content": self.content
        }

class GenerationInfo:
    """
    Represents information about content generation.

    Attributes:
        finish_reason (Optional[str]): The reason for finishing content generation.
    """

    def __init__(self, finish_reason: Optional[str] = None):
        self.finish_reason: Optional[str] = finish_reason

    def get_finish_reason(self) -> Optional[str]:
        return self.finish_reason

class TextDocument(KeyedContent):
    """
    Represents a text document with optional metadata.

    Attributes:
        key (str): The unique identifier for the content.
        content (str): The content data.
    """

    def __init__(self, key: str, content: str):
        super().__init__(key, content, ContentType.TEXT_DOCUMENT)
        self.document_type: DocumentType = DocumentType.TEXT
        self.metadata: DocumentMetadata = None

    def to_dict(self) -> Dict[str, Union[str, ContentType, DocumentType, Dict[str, Optional[Union[str, int]]]]]:
        return {
            "@type": "text_content",
            "key": self.key,
            "content_type": self.content_type.value,
            "content": self.content,
            "document_type": self.document_type.value,
            "metadata": self.metadata.to_dict() if self.metadata else None
        }

class DocumentMetadata:
    """
    Represents metadata associated with a document.

    Attributes:
        source (Optional[str]): The source of the document.
        pointer (Optional[int]): The pointer associated with the document.
    """

    def __init__(self):
        self.source: Optional[str] = None
        self.pointer: Optional[int] = None

    def get_source(self) -> Optional[str]:
        return self.source

    def get_pointer(self) -> Optional[int]:
        return self.pointer

    def to_dict(self) -> Dict[str, Optional[Union[str, int]]]:
        """
        Convert the metadata to a dictionary.

        Returns:
            Dict[str, Optional[Union[str, int]]]: The metadata represented as a dictionary.
        """
        metadata_dict = {
            "source": self.source,
            "pointer": self.pointer
        }
        # Remove fields with None values
        metadata_dict = {k: v for k, v in metadata_dict.items() if v is not None}
        return metadata_dict


