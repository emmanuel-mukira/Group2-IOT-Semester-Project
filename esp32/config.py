# =================================================
# config.py
# Central place for all settings that may change
# =================================================

from machine import unique_id
from ubinascii import hexlify


# =================================================
# CLOUD SETTINGS
# =================================================

# STAGE 2:
# Turn this ON when testing WiFi only, before MQTT or Firebase.
USE_WIFI = False

# STAGE 1:
# Keep MQTT OFF while testing sensors locally.
# Turn this ON later after local readings and WiFi work.
USE_MQTT = False

# STAGE 1:
# Keep Firebase OFF for now.
# Firebase comes last after WiFi + MQTT are working.
USE_FIREBASE = False


# CHANGE THIS:
# WiFi credentials for the hotspot/router the ESP32 will use.
WIFI_SSID = "K8597"
WIFI_PASSWORD = "00001111"


# MQTT SETTINGS
# CHANGE LATER:
# This is their local broker IP.
# Later we can change this to your broker or HiveMQ.
MQTT_BROKER = "192.168.137.89"
MQTT_PORT = 1883

# CHANGE LATER:
# This is their topic.
# Later we change it to your group topic.
MQTT_TOPIC = "iot/lab/sensor"

# Unique MQTT client ID for this ESP32.
MQTT_CLIENT_ID = b"esp32-iot-system-" + hexlify(unique_id())


# FIREBASE SETTINGS
# CHANGE LATER:
# Keep here for later, but Firebase stays OFF for now.
# Firebase Realtime Database URL must end with .json
FIREBASE_URL = "https://iot-vermiq-default-rtdb.firebaseio.com/latest_readings.json"


# =================================================
# PIN SETTINGS
# =================================================
# Keep the same structure as their code for now.
# We will remap later.

OLED_SDA = 18
OLED_SCL = 19

# One active DHT sensor pin.
# For DHT22
DHT_PIN = 27

MOISTURE_PIN = 32
PH_PIN = 33


# =================================================
# SENSOR SETTINGS
# =================================================

# CHANGE THIS depending on which sensor you want the code to read:
# "DHT11" for DHT11
# "DHT22" for DHT22
DHT_SENSOR_TYPE = "DHT22"


# =================================================
# CALIBRATION
# =================================================

# Use these later if the selected DHT sensor reads too high/low.
DHT_TEMP_OFFSET = 0.0
DHT_HUM_OFFSET = 0.0

# ESP32 ADC settings
ADC_MAX_VALUE = 4095
ADC_REFERENCE_VOLTAGE = 3.3
