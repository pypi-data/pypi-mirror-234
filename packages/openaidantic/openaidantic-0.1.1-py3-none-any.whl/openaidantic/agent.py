from .api import *
from .templating import *
from .utils import *


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
		response = await self.chat_completion.run(text,self.context.prompt)
		print(response.usage.json(indent=2))
		return response.choices[0].message.content
	
	async def instruction(self, text: str) -> str:
		response = await self.completion.run(text)
		print(response.usage.json(indent=2))
		return response.choices[0].text
	
	async def chat_streaming(self, text: str,context:str) -> AsyncGenerator[str, None]:
		input_tokens = count_tokens(text+context)
		outout_tokens = 0
		async for message in self.chat_completion.stream(text,context):
			outout_tokens += 1
			yield message
		usage = ChatCompletionUsage(prompt_tokens=input_tokens,completion_tokens=outout_tokens,total_tokens=input_tokens+outout_tokens)
		print(usage.json(indent=2))

	async def streaming(self, text: str) -> AsyncGenerator[str, None]:
		input_tokens = count_tokens(text)
		outout_tokens = 0
		async for message in self.completion.stream(text):
			outout_tokens += 1
			yield message
		usage = CompletionUsage(prompt_tokens=input_tokens,completion_tokens=outout_tokens,total_tokens=input_tokens+outout_tokens)
		print(usage.json(indent=2))
		
	async def generate_image(self, text: str, n:int=1) -> Union[str, List[str]]:
		return await self.image.run(text, n)
	
	async def transcribe_audio(self, audio:bytes)->str:
		return await self.audio.run(audio)
	
	async def create_embeddings(self, texts: List[str]) -> List[Vector]:
		return await self.embeddings.run(texts)