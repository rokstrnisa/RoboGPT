import os
import sys
import time
from typing import Optional
import openai
import tiktoken

openai.api_key = os.getenv("OPENAI_API_KEY")
MODEL = "gpt-4"
TOKEN_BUFFER = 50
COMBINED_TOKEN_LIMIT = 8192 - TOKEN_BUFFER
MAX_RESPONSE_TOKENS = 1000
MAX_REQUEST_TOKENS = COMBINED_TOKEN_LIMIT - MAX_RESPONSE_TOKENS
ENCODING = tiktoken.encoding_for_model(MODEL)
TOKENS_PER_MESSAGE = 3
TOKENS_PER_NAME = 1
USER_INPUT_SUFFIX = "Determine which next action to use, and write one valid action, a newline, and one valid metadata JSON object, both according to the specified schema:"


def chat(user_directions: str, general_directions: str, new_plan: Optional[str], message_history):
    system_message_content = f"{user_directions}\n{general_directions}"
    system_message = {"role": "system", "content": system_message_content}
    user_message_content = USER_INPUT_SUFFIX
    if new_plan is not None:
        user_message_content = f"Change your plan to: {new_plan}\n{user_message_content}"
    user_message = {"role": "user", "content": user_message_content}
    messages = [system_message, user_message]
    insert_history_at = len(messages) - 1
    request_token_count = count_tokens(messages)
    for message in reversed(message_history):
        message_token_count = count_tokens([message])
        if request_token_count + message_token_count > MAX_REQUEST_TOKENS:
            break
        request_token_count += message_token_count
        messages.insert(insert_history_at, message)
    available_response_tokens = COMBINED_TOKEN_LIMIT - request_token_count
    # print("=== MESSAGES START ===")
    # for message in messages:
    #     print(message["role"], message["content"][:100], count_tokens([message]))
    # print("=== MESSAGES END ===")
    # print(f"available_response_tokens: {available_response_tokens}")
    assistant_response = send_message(messages, available_response_tokens)
    message_history.append(user_message)
    message_history.append({"role": "assistant", "content": assistant_response})
    return assistant_response


def count_tokens(messages) -> int:
    token_count = 0
    for message in messages:
        token_count += TOKENS_PER_MESSAGE
        for key, value in message.items():
            token_count += len(ENCODING.encode(value))
            if key == "name":
                token_count += TOKENS_PER_NAME
    token_count += 3
    return token_count


def send_message(messages, max_response_tokens: int) -> str:
    while True:
        try:
            response = openai.ChatCompletion.create(model=MODEL, messages=messages, max_tokens=max_response_tokens)
            return response.choices[0].message["content"]  # type: ignore
        except openai.error.RateLimitError:  # type: ignore
            print(f"Model {MODEL} currently overloaded. Waiting 10 seconds...")
            time.sleep(10)
