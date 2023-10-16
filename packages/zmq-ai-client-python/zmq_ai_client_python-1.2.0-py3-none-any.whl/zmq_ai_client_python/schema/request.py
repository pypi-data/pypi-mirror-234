from dataclasses import dataclass
from enum import Enum
from typing import List, Optional, Dict

from zmq_ai_client_python.schema.completion import Message, Function


class RequestType(Enum):
    CHAT_COMPLETION_REQUEST = 0x01
    SESSION_STATE_REQUEST = 0x02
    TITLE_GENERATION_REQUEST = 0x03


@dataclass
class ChatCompletionRequest:
    """
    Dataclass representing a chat completion request to the model.
    """
    model: str  # Name of the model to be used
    messages: List[Message]  # List of messages in the request
    functions: Optional[List[Function]] = None  # Optional list of functions in the request
    temperature: Optional[float] = 1.0  # Sampling temperature for the model's output
    top_p: Optional[float] = 1.0  # Nucleus sampling parameter
    n: Optional[int] = 1  # Number of completions to generate
    stream: Optional[bool] = False  # Whether to stream the output
    stop: Optional[List[str]] = None  # List of tokens to stop the generation
    max_tokens: Optional[int] = 256  # Maximum number of tokens in the output
    presence_penalty: Optional[float] = 0.0  # Penalty for new tokens in the output
    frequency_penalty: Optional[float] = 0.0  # Penalty for frequent tokens in the output
    logit_bias: Optional[dict] = None  # Bias for certain tokens in the output
    user: Optional[str] = None  # Optional user identifier for the request
    key_values: Optional[Dict[str, str]] = None  # Optional key_values for advanced options


@dataclass
class SessionStateRequest:
    """
    Dataclass representing a session cache request to the model.
    """
    session_id: str
    user_id: str


@dataclass
class TitleGenerationRequest:
    """
    Dataclass representing a title generation request to the model.
    """
    model: str  # Name of the model to be used
    messages: List[Message]  # List of messages in the request
    functions: Optional[List[Function]] = None  # Optional list of functions in the request
    temperature: Optional[float] = 1.0  # Sampling temperature for the model's output
    top_p: Optional[float] = 1.0  # Nucleus sampling parameter
    n: Optional[int] = 1  # Number of completions to generate
    stream: Optional[bool] = False  # Whether to stream the output
    stop: Optional[List[str]] = None  # List of tokens to stop the generation
    max_tokens: Optional[int] = 256  # Maximum number of tokens in the output
    presence_penalty: Optional[float] = 0.0  # Penalty for new tokens in the output
    frequency_penalty: Optional[float] = 0.0  # Penalty for frequent tokens in the output
    logit_bias: Optional[dict] = None  # Bias for certain tokens in the output
