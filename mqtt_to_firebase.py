import json
import os
import time
from datetime import datetime, timezone

import requests
import paho.mqtt.client as mqtt


MQTT_BROKER = os.getenv("MQTT_BROKER", "127.0.0.1")
MQTT_PORT = int(os.getenv("MQTT_PORT", "1883"))
MQTT_TOPIC = os.getenv("MQTT_TOPIC", "iot/group2/project")

FIREBASE_BASE_URL = os.getenv(
    "FIREBASE_BASE_URL",
    "https://iot-project-group-2-72c7b-default-rtdb.europe-west1.firebasedatabase.app",
).rstrip("/")

LATEST_URL = FIREBASE_BASE_URL + "/latest_reading.json"
HISTORY_URL = FIREBASE_BASE_URL + "/readings.json"


def utc_now():
    return datetime.now(timezone.utc).isoformat()


def publish_to_firebase(payload):
    payload["received_at"] = utc_now()

    latest_response = requests.put(LATEST_URL, json=payload, timeout=10)
    latest_response.raise_for_status()

    history_response = requests.post(HISTORY_URL, json=payload, timeout=10)
    history_response.raise_for_status()


def on_connect(client, userdata, flags, reason_code, properties=None):
    if reason_code == 0:
        print("MQTT bridge connected")
        print("Subscribing to:", MQTT_TOPIC)
        client.subscribe(MQTT_TOPIC)
    else:
        print("MQTT bridge connection failed:", reason_code)


def on_message(client, userdata, message):
    try:
        payload_text = message.payload.decode("utf-8")
        payload = json.loads(payload_text)

        print("MQTT message received:", payload_text)
        publish_to_firebase(payload)
        print("Firebase updated")

    except Exception as e:
        print("Bridge error:", e)


def main():
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    client.on_connect = on_connect
    client.on_message = on_message

    while True:
        try:
            print("Connecting MQTT bridge to", MQTT_BROKER, "port", MQTT_PORT)
            client.connect(MQTT_BROKER, MQTT_PORT, keepalive=60)
            client.loop_forever()
        except KeyboardInterrupt:
            print("Bridge stopped")
            break
        except Exception as e:
            print("MQTT bridge error:", e)
            time.sleep(5)


if __name__ == "__main__":
    main()
