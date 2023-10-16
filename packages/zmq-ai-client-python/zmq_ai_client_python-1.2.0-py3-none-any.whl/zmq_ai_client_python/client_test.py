import json
from dataclasses import asdict

from zmq_ai_client_python.client import LlamaClient
from zmq_ai_client_python.schema.completion import ChatCompletion
from zmq_ai_client_python.schema.request import Message, ChatCompletionRequest, SessionStateRequest
from zmq_ai_client_python.schema.session_state import SessionStateResponse


def main():
    client = LlamaClient('tcp://localhost:5555')
    session_id = "6eef38d9-1c7f-4314-9d41-54271ef97f17"
    user_id = "708bab67-64d2-4e7d-94b6-2b6e043d8844"

    messages = [
        Message(role='user', content='What is the capital of france?'),
        Message(role='assistant', content='The capital of France is Paris'),
        Message(role='user', content='Can you tell me about Flask framework?')

    ]
    STOP = ["\n###Human"]
    request = ChatCompletionRequest(
        model='gpt-3.5-turbo',
        messages=messages,
        temperature=0.8,
        n=256,
        stop=STOP,
        user=user_id,
        key_values={"session": session_id}
    )

    session_request = SessionStateRequest(
        session_id=session_id,
        user_id=user_id
    )

    json_str = json.dumps(asdict(session_request), indent=4)
    print(json_str)

    session_state_response: SessionStateResponse = client.send_session_state_request(session_request)

    json_str = json.dumps(asdict(session_state_response), indent=4)
    print(json_str)

    json_str = json.dumps(asdict(request), indent=4)
    print(json_str)

    chat_response: ChatCompletion = client.send_chat_completion_request(request)

    json_str = json.dumps(asdict(chat_response), indent=4)
    print(json_str)


if __name__ == "__main__":
    main()
