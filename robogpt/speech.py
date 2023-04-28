import os
import tempfile
from threading import Thread
import requests
from playsound import playsound


BASE_URL = "https://api.elevenlabs.io/v1/text-to-speech"
VOICE_ID = "ErXwobaYiN019PkySvjV"
API_URL = f"{BASE_URL}/{VOICE_ID}"
API_KEY = os.getenv("ELEVENLABS_API_KEY")


def say_async(text: str) -> None:
    Thread(target=say, args=[text]).start()


def say(text: str) -> None:
    headers = {"Content-Type": "application/json", "xi-api-key": API_KEY}
    data = {"text": text}
    response = requests.post(API_URL, headers=headers, json=data, timeout=10)
    if response.status_code == 200:
        with tempfile.NamedTemporaryFile(mode="wb") as temp:
            temp.write(response.content)
            temp.flush()
            playsound(temp.name)
    else:
        print(f"Failed to speak: status code = {response.status_code}\n{response.content}")
