# =================================================
# main.py
# Main program controller
# Current stage:
# Local OLED + sensor testing
# =================================================

import time

from config import (
    USE_WIFI,
    USE_MQTT,
    USE_FIREBASE,
    DHT_PIN,
    MOISTURE_PIN,
    PH_PIN
)

from oled_display import (
    init_oled,
    oled_message,
    display_sensor_data,
    display_error
)

from sensors import (
    init_sensors,
    read_dht,
    read_moisture,
    read_ph
)

from wifi_manager import connect_wifi
from mqtt_manager import connect_mqtt, publish_mqtt
from firebase_client import publish_firebase


# =================================================
# INITIAL SETUP
# =================================================

client = None

init_oled()

init_sensors()

wifi_connected = False

# WiFi starts for standalone WiFi tests or when cloud features are enabled.
if USE_WIFI or USE_MQTT or USE_FIREBASE:
    wifi_connected = connect_wifi()

    if wifi_connected and USE_MQTT:
        client = connect_mqtt()

    if not wifi_connected:
        print("Cloud features disabled because WiFi failed.")
        oled_message("Cloud Disabled", "WiFi failed")


print("Starting IoT system...")
print("OLED enabled")
print("DHT22 on GPIO", DHT_PIN)
print("Moisture on GPIO", MOISTURE_PIN)
print("pH on GPIO", PH_PIN)
print("--------------------------------------")

oled_message(
    "System Ready",
    "DHT22 GPIO" + str(DHT_PIN),
    "Moisture + pH"
)

time.sleep(2)


# =================================================
# MAIN LOOP
# =================================================

while True:
    try:
        dht_temp, dht_hum = read_dht()

        moisture_raw, moisture_percent = read_moisture()

        ph_raw, ph_voltage, ph = read_ph()

        print("========== SENSOR READINGS ==========")
        print("Air Temp      :", round(dht_temp, 2), "C")
        print("Humidity      :", round(dht_hum, 2), "%")
        print("Moisture Raw  :", moisture_raw)
        print("Moisture      :", round(moisture_percent, 2), "%")
        print("pH Raw        :", ph_raw)
        print("pH Voltage    :", round(ph_voltage, 3), "V")
        print("pH Value      :", round(ph, 2))
        print("Sensor Type   :", "DHT22")
        print("=====================================")

        display_sensor_data(
            dht_temp,
            dht_hum,
            moisture_percent,
            ph,
            ph_voltage
        )

        payload = {
            "device": "ESP32-IOT-SYSTEM",
            "dht_sensor_type": "DHT22",
            "temperature": dht_temp,
            "humidity": dht_hum,
            "moisture_raw": moisture_raw,
            "moisture_percent": round(moisture_percent, 2),
            "ph_raw": ph_raw,
            "ph_voltage": round(ph_voltage, 3),
            "ph": round(ph, 2),
            "uptime": time.ticks_ms() // 1000
        }

        # MQTT is OFF for now.
        # Later turn on by setting USE_MQTT = True in config.py.
        if USE_MQTT and client is not None:
            publish_mqtt(client, payload)

        # Firebase is OFF for now.
        # Later turn on by setting USE_FIREBASE = True in config.py.
        if USE_FIREBASE and wifi_connected:
            publish_firebase(payload)

    except Exception as e:
        print("Main loop error:", e)
        display_error(e)

    time.sleep(3)
