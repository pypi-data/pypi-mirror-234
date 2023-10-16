import json
import pytest
from dataclasses import asdict

from zmq_ai_client_python.client import LlamaClient
from zmq_ai_client_python.schema.completion import ChatCompletion
from zmq_ai_client_python.schema.request import Message, ChatCompletionRequest, SessionStateRequest, \
    TitleGenerationRequest
from zmq_ai_client_python.schema.session_state import SessionStateResponse


@pytest.fixture
def setup_client():
    client = LlamaClient('tcp://localhost:5555')
    return client


@pytest.fixture
def setup_chat_completion_request() -> ChatCompletionRequest:
    session_id = "6eef38d9-1c7f-4314-9d41-54271ef97f17"
    user_id = "708bab67-64d2-4e7d-94b6-2b6e043d8844"
    messages = [
        Message(role='system', content='You are a helpful assistant'),
        Message(role='user', content="What is the capital of Turkey?")
    ]
    STOP = ["\n ###Human"]
    return ChatCompletionRequest(
        model='vicuna7b-1.5',
        messages=messages,
        temperature=0.8,
        n=256,
        stop=STOP,
        user=user_id,
        key_values={"session": session_id}
    )


@pytest.fixture
def setup_session_state_request() -> SessionStateRequest:
    session_id = "6eef38d9-1c7f-4314-9d41-54271ef97f17"
    user_id = "708bab67-64d2-4e7d-94b6-2b6e043d8844"
    return SessionStateRequest(
        session_id=session_id,
        user_id=user_id
    )


@pytest.fixture
def setup_title_generation_request() -> TitleGenerationRequest:
    messages = [
        Message(
            role="system",
            content="You are a helpful assistant. You generate a descriptive, short and meaningful title for the given "
                    "conversation.",
        ),
        Message(
            role="user",
            content=f"Question: What is the capital of France? Answer: The capital of France is Paris"
        )
    ]
    STOP = ["\n ###Human"]
    return TitleGenerationRequest(
        model='vicuna7b-1.5',
        messages=messages,
        temperature=0.8,
        n=256,
        stop=STOP,
    )


def print_json(data):
    json_str = json.dumps(asdict(data), indent=4)
    print(json_str)


def test_session_state_request(setup_client, setup_session_state_request):
    response: SessionStateResponse = setup_client.send_session_state_request(setup_session_state_request)
    assert response, "No session state response received."
    print_json(response)


def test_chat_completion_request(setup_client, setup_chat_completion_request):
    response: ChatCompletion = setup_client.send_chat_completion_request(setup_chat_completion_request)
    assert response, "No chat completion response received."
    print_json(response)


def test_title_generation_request(setup_client, setup_title_generation_request):
    response: ChatCompletion = setup_client.send_title_generation_request(setup_title_generation_request)
    assert response, "No chat completion response received."
    print_json(response)


if __name__ == "__main__":
    pytest.main()
