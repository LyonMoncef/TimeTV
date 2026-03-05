import os
import sys
import time

import requests
from dotenv import load_dotenv

import bot_core

load_dotenv()

SIGNAL_NUMBER = os.environ.get("SIGNAL_NUMBER")
SIGNAL_API_URL = os.environ.get("SIGNAL_API_URL", "http://localhost:8080")

if not SIGNAL_NUMBER:
    print("SIGNAL_NUMBER not set", file=sys.stderr)
    sys.exit(1)


def receive():
    r = requests.get(f"{SIGNAL_API_URL}/v1/receive/{SIGNAL_NUMBER}", timeout=10)
    r.raise_for_status()
    return r.json()


def send(recipient: str, text: str):
    requests.post(f"{SIGNAL_API_URL}/v2/send", json={
        "message": text,
        "number": SIGNAL_NUMBER,
        "recipients": [recipient],
    }, timeout=10)


def run():
    print(f"Signal bot polling on {SIGNAL_NUMBER}")
    while True:
        try:
            messages = receive()
            for msg in messages:
                envelope = msg.get("envelope", {})
                data_message = envelope.get("dataMessage")
                if not data_message:
                    continue
                text = data_message.get("message", "").strip()
                if not text:
                    continue
                sender = envelope.get("source")
                if not sender:
                    continue
                reply = bot_core.chat(sender, text)
                send(sender, reply)
        except Exception as e:
            print(f"Error: {e}", file=sys.stderr)
        time.sleep(2)


if __name__ == "__main__":
    run()
