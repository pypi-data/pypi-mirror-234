from .api import CompletionResponse, CompletionStreamResponse
from .base_completion import BaseCompletion


class Completion(BaseCompletion):
    """
    Class for handling text completions.
    """

    endpoint = "completions"
    response_class = CompletionResponse
    stream_response_class = CompletionStreamResponse

    @classmethod
    def _get_data_key(cls) -> str:
        return "prompt"
