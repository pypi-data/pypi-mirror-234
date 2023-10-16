from tempfile import NamedTemporaryFile
from typing import Any, Set, Type

from pydantic import Field, root_validator  # pylint: disable=no-name-in-module

from .helpers import count_tokens
from .typedefs import AudioFormat  # pylint: disable=no-name-in-module
from .typedefs import (BaseModel, ChatModel, CompletionModel, Dict,
                       ImageFormat, List, Role, Size)


class CompletionRequest(BaseModel):
    model: CompletionModel = Field(default="gpt-3.5-turbo-instruct")
    prompt: str = Field(...)
    temperature: float = Field(default=0.2)
    max_tokens: int = Field(default=1024)
    stream: bool = Field(default=False)


class CompletionChoice(BaseModel):
    index: int = Field(...)
    finish_reason: str = Field(...)
    text: str = Field(...)


class CompletionUsage(BaseModel):
    prompt_tokens: int = Field(...)
    completion_tokens: int = Field(...)
    total_tokens: int = Field(...)


class CompletionResponse(BaseModel):
    id: str = Field(...)
    object: str = Field(...)
    created: int = Field(...)
    model: CompletionModel = Field(...)
    choices: List[CompletionChoice] = Field(...)
    usage: CompletionUsage = Field(...)


class Message(BaseModel):
    """
    Represents a message within the chatcompletion API pipeline.
    """

    role: Role = Field(default="user")
    content: str = Field(...)


class ChatCompletionRequest(BaseModel):
    model: ChatModel = Field(default="gpt-3.5-turbo-16k")
    messages: List[Message] = Field(...)
    temperature: float = Field(default=0.5)
    max_tokens: int = Field(default=4096)
    stream: bool = Field(default=False)


class ChatCompletionUsage(BaseModel):
    """Token usage statistics for a chat completion API call."""

    prompt_tokens: int = Field(...)
    completion_tokens: int = Field(...)
    total_tokens: int = Field(...)


class ChatCompletionChoice(BaseModel):
    index: int = Field(...)
    message: Message = Field(...)
    finish_reason: str = Field(...)


class ChatCompletionResponse(BaseModel):
    id: str = Field(...)
    object: str = Field(...)
    created: int = Field(...)
    model: str = Field(...)
    choices: List[ChatCompletionChoice] = Field(...)
    usage: ChatCompletionUsage = Field(...)


class EmbeddingUssage(BaseModel):
    """Token usage statistics for an embedding API call."""

    prompt_tokens: int = Field(...)
    total_tokens: int = Field(...)


class CreateImageResponse(BaseModel):
    created: float = Field(...)
    data: List[Dict[ImageFormat, str]] = Field(...)


class CreateImageRequest(BaseModel):
    """Request to create an image from a prompt. Use default values for configuration unless specified."""

    prompt: str = Field(...)
    n: int = Field(default=1)
    size: Size = Field(default="1024x1024")
    response_format: ImageFormat = Field(default="url")


class FineTuneSample(BaseModel):
    messages: List[Message] = Field(..., max_items=3, min_items=2)

    @root_validator
    @classmethod
    def check_messages(cls: Type[BaseModel], values: Dict[str, Any]):
        roles: Set[Role] = set()
        for message in values["messages"]:
            roles.add(message.role)
        assert len(roles) == len(
            values["messages"]
        ), "All messages must be from different roles."
        return values


class FineTuneRequest(BaseModel):
    __root__: List[FineTuneSample] = Field(..., min_items=10, max_items=100000)

    def __call__(self):
        with NamedTemporaryFile("w", suffix=".json") as f:
            data = self.json()
            assert count_tokens(data) < 4096, "Data too large."
            f.write(data)
            f.flush()
            return f


class AudioRequest(BaseModel):
    file: bytes = Field(...)
    format: AudioFormat = Field(default="mp3")

    def __call__(self):
        with NamedTemporaryFile("wb", suffix=f".{self.format}") as f:
            f.write(self.file)
            f.flush()
            assert len(f.read()) < 25 * 1024 * 1024, "File too large."
            return f
