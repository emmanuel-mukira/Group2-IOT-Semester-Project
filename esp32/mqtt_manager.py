import time
import ujson

from config import (
    MQTT_CLIENT_ID,
    MQTT_BROKER,
    MQTT_PORT,
    MQTT_TOPIC
)

from oled_display import oled_message


try:
    from umqtt.simple import MQTTClient
except:
    MQTTClient = None


def connect_mqtt():
    """
    Connects ESP32 to the configured MQTT broker.
    """

    if MQTTClient is None:
        print("MQTT library not available")
        return None

    try:
        client = MQTTClient(
            client_id=MQTT_CLIENT_ID,
            server=MQTT_BROKER,
            port=MQTT_PORT,
            keepalive=60
        )

        client.connect()

        print("MQTT connected")
        oled_message("MQTT Connected", "Ready")
        time.sleep(1)

        return client

    except Exception as e:
        print("MQTT connection failed:", e)
        oled_message("MQTT Failed", str(e)[:16])

        return None


def publish_mqtt(client, payload):
    """
    Publishes JSON payload to MQTT topic.
    """

    if client is None:
        print("MQTT client is not connected")
        return False

    try:
        client.publish(MQTT_TOPIC, ujson.dumps(payload))
        print("MQTT published")

        return True

    except Exception as e:
        print("MQTT publish failed:", e)

        return False
