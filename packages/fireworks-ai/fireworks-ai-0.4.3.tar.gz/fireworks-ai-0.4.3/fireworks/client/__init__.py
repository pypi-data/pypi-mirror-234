import os
from .completion import Completion
from .chat_completion import ChatCompletion
from .model import Model

with open(
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "VERSION"), "r"
) as f:
    __version__ = f.read().strip()

api_key = os.environ.get("FIREWORKS_API_KEY")
base_url = os.environ.get("FIREWORKS_API_BASE", "https://api.fireworks.ai/inference/v1")

__all__ = [
    "__version__",
    "ChatCompletion",
    "Completion",
    "Model",
]
