from .api import *
from .templating import *


class Agent(BaseModel, ABC):
	chat_completion: ChatCompletion = Field(default_factory=ChatCompletion)
	completion: Completion = Field(default_factory=Completion)
	embeddings: Embeddings = Field(default_factory=Embeddings)
	audio: Audio = Field(default_factory=Audio)
	image: Image = Field(default_factory=Image)
	context: TemplateModel = Field(default_factory=TemplateModel)

	@abstractmethod
	async def run(self, text: str) -> Any:
		raise NotImplementedError


class OpenAIAgent(Agent):
	@override
	async def run(self, text: str):
		print(self.context.prompt)
		return await self.chat_completion.run(text,self.context.prompt)
	
	async def stream_chat(self, text: str,context:str) -> AsyncGenerator[str, None]:
		async for message in self.chat_completion.stream(text,context):
			yield message

	async def stream_completion(self, text: str) -> AsyncGenerator[str, None]:
		async for message in self.completion.stream(text):
			yield message

	async def generate_image(self, text: str, n:int=1) -> Union[str, List[str]]:
		return await self.image.run(text, n)
	
	async def transcribe_audio(self, audio:bytes)->str:
		return await self.audio.run(audio)
	
	async def create_embeddings(self, texts: List[str]) -> List[Vector]:
		return await self.embeddings.run(texts)