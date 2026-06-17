from machine import unique_id
from ubinascii import hexlify


USE_WIFI = True
USE_MQTT = True
USE_FIREBASE = True


WIFI_SSID = "bk"
WIFI_PASSWORD = "12345678"


# MQTT SETTINGS
MQTT_BROKER = "192.168.137.77"
MQTT_PORT = 1883
MQTT_TOPIC = "iot/group2/project"

MQTT_CLIENT_ID = b"esp32-iot-system-" + hexlify(unique_id())


# FIREBASE SETTINGS
# Firebase Realtime Database URL must end with .json
FIREBASE_URL = "https://iot-project-group-2-72c7b-default-rtdb.europe-west1.firebasedatabase.app/.json"


# PIN SETTINGS
OLED_SDA = 21
OLED_SCL = 22

DHT_PIN = 4

MOISTURE_PIN = 32
PH_PIN = 33


# SENSOR SETTINGS
DHT_SENSOR_TYPE = "DHT22"


# CALIBRATION
MOISTURE_DRY_RAW = 100
MOISTURE_WET_RAW = 40

DHT_TEMP_OFFSET = -5.0
DHT_HUM_OFFSET = 20.0

PH_NEUTRAL_VOLTAGE = 2.5
PH_SLOPE = -5.7

ADC_MAX_VALUE = 4095
ADC_REFERENCE_VOLTAGE = 3.3

