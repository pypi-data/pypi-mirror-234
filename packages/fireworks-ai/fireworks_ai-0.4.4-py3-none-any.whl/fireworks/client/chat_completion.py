from .api import ChatCompletionResponse, ChatCompletionStreamResponse
from .base_completion import BaseCompletion


class ChatCompletion(BaseCompletion):
    """
    Class for handling chat completions.
    """

    endpoint = "chat/completions"
    response_class = ChatCompletionResponse
    stream_response_class = ChatCompletionStreamResponse

    @classmethod
    def _get_data_key(cls) -> str:
        return "messages"
