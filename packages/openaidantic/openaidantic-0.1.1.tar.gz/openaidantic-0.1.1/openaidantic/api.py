from typing import AsyncGenerator

import openai
from typing_extensions import override

from .costs import *
from .functions import *
from .schema import *
from .typedefs import *
from .utils import *


class ChatCompletion(OpenAIResource):
    model: ChatModel = Field(default="gpt-3.5-turbo")

    @exponential_backoff()
    async def run(self, text: str, context: str):  # type: ignore
        request = ChatCompletionRequest(
            messages=[Message(content=text), Message(content=context, role="system")]
        )
        response = await openai.ChatCompletion.acreate(**request.dict())  # type: ignore
        return ChatCompletionResponse(**response)  # type: ignore

    async def stream(self, text: str, context: str) -> AsyncGenerator[str, None]:
        request = ChatCompletionRequest(
            messages=[Message(content=text), Message(content=context, role="system")],
            stream=True,
        )
        response = await openai.ChatCompletion.acreate(**request.dict())  # type: ignore
        async for message in response:  # type: ignore
            data = message.choices[0].delta.get("content",None) # type: ignore
            yield data # type: ignore



class Completion(OpenAIResource):
    model: CompletionModel = Field(default="gpt-3.5-turbo-instruct")

    @exponential_backoff()
    async def run(self, text: str):  # type: ignore
        request = CompletionRequest(prompt=text)
        response = await openai.Completion.acreate(**request.dict())  # type: ignore
        usage = CompletionUsage(**response.usage)  # type: ignore
        return CompletionResponse(**response)  # type: ignore

    async def stream(self, text: str) -> AsyncGenerator[str, None]:
        request = CompletionRequest(prompt=text, stream=True)
        response = await openai.Completion.acreate(**request.dict())  # type: ignore
        async for message in response:  # type: ignore
            data = message.choices[0].get("text",None)  # type: ignore
            yield data # type: ignore
    

class Embeddings(OpenAIResource):
    model: EmbeddingModel = Field(default="text-embedding-ada-002")

    @exponential_backoff()
    async def run(self, texts: List[str]) -> List[Vector]:  # type: ignore
        response = await openai.Embedding.acreate(input=texts, model=self.model)  # type: ignore
        print(response)
        return [r.embedding for r in response.data]  # type: ignore


class Image(OpenAIResource):
    model: ImageModel = Field(default="dall-e")
    size: Size = Field(default="1024x1024")
    format: ImageFormat = Field(default="url")

    @exponential_backoff()
    async def run(self, text: str, n: int = 1) -> Union[List[str], str]:  # type: ignore
        response = await openai.Image.acreate(prompt=text, n=n, size=self.size, response_format=self.format)  # type: ignore
        print(response)
        if len(response.data) == 1:  # type: ignore
            return [response.data[0][self.format]]  # type: ignore
        return [r[self.format] for r in response.data]  # type: ignore


class Audio(OpenAIResource):
    model: AudioModel = Field(default="whisper-1")

    @exponential_backoff()
    async def run(self, content: bytes, audioformat: AudioFormat = "wav") -> str:  # type: ignore
        response = await openai.Audio.acreate(self.model, AudioRequest(file=content, format=audioformat)())  # type: ignore
        print(response)
        return response.get("text", "")  # type: ignore
