from .typedefs import ChatModel, Size


def image_cost(size: Size, quantity: int) -> float:
    """Calculates the cost of an Image API call."""
    if size == "1024x1024":
        return 0.02 * quantity
    elif size == "512x512":
        return 0.018 * quantity
    elif size == "256x256":
        return 0.016 * quantity


def audio_cost(duration: int) -> float:
    """Calculates the cost of an Audio API call."""
    return duration * 0.006 / round(duration / 60)


def chat_completion_cost(
    input_tokens: int, output_tokens: int, model: ChatModel
) -> float:
    """Calculates the cost of a chat completion API call."""
    if model == "gpt-4":
        return input_tokens * 0.03 / 1000 + output_tokens * 0.06 / 1000
    elif model == "gpt-3.5-turbo":
        return input_tokens * 0.0015 / 1000 + output_tokens * 0.002 / 1000
    elif model == "gpt-3.5-turbo-16k":
        return input_tokens * 0.003 / 1000 + output_tokens * 0.004 / 1000
    else:
        raise ValueError(f"Invalid model: {model}")


def embeddings_cost(tokens: int) -> float:
    """Calculates the cost of an Embeddings API call."""
    return tokens * 0.0001 / 1000


def completion_cost(tokens: int) -> float:
    """Calculates the cost of a Davinci 002 API call."""
    return tokens * 0.0020 / 1000
