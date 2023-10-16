import json
from abc import ABC, abstractmethod
from typing import Any

from pydantic import BaseModel, Field

from .api import *
from .helpers import *
from .helpers import count_tokens, get_duration
from .lib import *
from .templating import *

logger = setup_logging(__name__)

class Agent(BaseModel, ABC):
    """
    Base class for creating conversational agents.

    Attributes:
    -----------
    name : str
        Name of the agent.
    chat_completion : ChatCompletion
        Chat completion model used by the agent.
    completion : Completion
        Completion model used by the agent.
    embeddings : Embeddings
        Embeddings model used by the agent.
    audio : Audio
        Audio model used by the agent.
    image : Image
        Image model used by the agent.
    context : TemplateModel
        Template model used by the agent.

    Methods:
    --------
    memory() -> MemoryProtocol:
        Abstract method to get the memory of the agent.
    async run(text: str) -> Any:
        Abstract method to run the agent with the given text input.
    """
    name: str = Field(...)
    chat_completion: ChatCompletion = Field(default_factory=ChatCompletion)
    completion: Completion = Field(default_factory=Completion)
    embeddings: Embeddings = Field(default_factory=Embeddings)
    audio: Audio = Field(default_factory=Audio)
    image: Image = Field(default_factory=Image)
    context: TemplateModel = Field(default_factory=TemplateModel)

    @property
    @abstractmethod
    def memory(self) -> MemoryProtocol:
        ...

    @abstractmethod
    async def run(self, text: str) -> Any:
        raise NotImplementedError


class OpenAIAgent(Agent):
    @property
    def memory(self):
        return SqliteMemory(self.name)

    @override
    async def run(self, text: str):
        response = await self.chat_completion.run(text, self.context.prompt)
        logger.info(response.json(indent=2))
        data =response.choices[0].message.content
        await self.memory.save_chat_completion_usage(response.usage)
        await self.memory.upsert([Message(content=text, role="user"), Message(content=data, role="assistant")])
        return data

    async def instruction(self, text: str) -> str:
        response = await self.completion.run(text)
        logger.info(response.json(indent=2))
        await self.memory.save_completion_usage(response.usage)
        return response.choices[0].text

    async def chat_streaming(
        self, text: str, context: str
    ) -> AsyncGenerator[str, None]:
        input_tokens = count_tokens(text + context)
        outout_tokens = 0
        complete_string:str =""
        async for message in self.chat_completion.stream(text, context):
            outout_tokens += 1
            complete_string += message
            yield message
        usage = ChatCompletionUsage(
            prompt_tokens=input_tokens,
            completion_tokens=outout_tokens,
            total_tokens=input_tokens + outout_tokens,
        )
        await self.memory.save_chat_completion_usage(usage)
        await self.memory.upsert([Message(content=text, role="user"), Message(content=complete_string, role="assistant")])
    async def streaming(self, text: str) -> AsyncGenerator[str, None]:
        input_tokens = count_tokens(text)
        outout_tokens = 0
        async for message in self.completion.stream(text):
            outout_tokens += 1
            yield message
        usage = CompletionUsage(
            prompt_tokens=input_tokens,
            completion_tokens=outout_tokens,
            total_tokens=input_tokens + outout_tokens,
        )
        await self.memory.save_completion_usage(usage)

    async def generate_image(self, text: str, n: int = 1) -> List[str]:
        response = await self.image.run(text, n)  # type: ignore
        logger.info(json.dumps(response, indent=2)) # type: ignore
        await self.memory.save_image(text, response[0])
        return response

    async def transcribe_audio(self, audio: bytes) -> str:
        response = await self.audio.run(audio)
        logger.info(response)
        duration = get_duration(audio)
        await self.memory.save_audio(duration, response)
        return response
    
    async def create_embeddings(self, texts: List[str]) -> List[Vector]:
        response = await self.embeddings.run(texts)
        logger.info("%s embeddings created.", len(response))
        await self.memory.save_embeddings_usage(EmbeddingUssage(
            prompt_tokens=sum([count_tokens(text) for text in texts]),
            total_tokens=sum([count_tokens(text) for text in texts])         )
        )
        return response