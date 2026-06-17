# Group 2 IoT Vermiculture Monitoring System

We built an ESP32-based IoT monitoring system for a vermiculture bed. The system read air temperature, humidity, soil moisture, and pH values, displayed the live readings on an OLED screen, published readings over MQTT, and uploaded readings to Firebase Realtime Database for later dashboard use.

The final implementation used MicroPython on the ESP32 and kept the firmware split into small files so each part of the system was easier to test and maintain.

## Features We Completed

- Read temperature and humidity using a DHT22 sensor.
- Read soil moisture using an analog soil moisture sensor.
- Read pH voltage and calculated pH using a PH-4502C sensor.
- Displayed live sensor readings on an SH1106 OLED display.
- Connected the ESP32 to WiFi.
- Published sensor payloads to an MQTT topic.
- Uploaded sensor payloads to Firebase Realtime Database.
- Saved cleaned lab readings in text and Firebase-ready JSON formats.

## Hardware Used

- ESP32 development board
- DHT22 temperature and humidity sensor
- Analog soil moisture sensor
- PH-4502C pH sensor module
- SH1106 128x64 I2C OLED display
- 10k ohm pull-up resistor for the DHT22 data line
- Breadboard and jumper wires

## Final Pin Mapping

The final pin mapping came from `esp32/config.py`.

| Component | Signal | ESP32 Pin |
|---|---:|---:|
| OLED display | SDA | GPIO21 |
| OLED display | SCL | GPIO22 |
| DHT22 | DATA | GPIO4 |
| Soil moisture sensor | AOUT | GPIO32 |
| PH-4502C | Po | GPIO33 |

Power connections used the ESP32 3V3/GND rails for the DHT22, OLED, and soil moisture sensor. The pH module used VIN/5V and GND.

## Firmware Structure

```txt
esp32/main.py              Main program loop
esp32/config.py            WiFi, MQTT, Firebase, pin, and calibration settings
esp32/sensors.py           DHT22, soil moisture, and pH reading functions
esp32/oled_display.py      OLED setup and display helper functions
esp32/sh1106.py            SH1106 OLED driver
esp32/wifi_manager.py      WiFi connection logic
esp32/mqtt_manager.py      MQTT connection and publish logic
esp32/firebase_client.py   Firebase upload logic
```

The main loop read the sensors every few seconds, printed the readings, updated the OLED, prepared a JSON payload, published it to MQTT, and sent it to Firebase when WiFi was connected.

## Network and Cloud Setup

The ESP32 connected to WiFi using the credentials in `esp32/config.py`.

```python
USE_WIFI = True
USE_MQTT = True
USE_FIREBASE = True

MQTT_BROKER = "192.168.137.77"
MQTT_PORT = 1883
MQTT_TOPIC = "iot/group2/project"
```

Firebase uploads used the Realtime Database REST URL configured in `FIREBASE_URL`. The ESP32 sent the latest payload using `PUT`, and the cleaned JSON dataset was prepared for Firebase import and dashboard fetching.

## Reading Payload

Each reading payload contained:

```json
{
  "device": "ESP32-IOT-SYSTEM",
  "dht_sensor_type": "DHT22",
  "temperature": 22.9,
  "humidity": 61.4,
  "moisture_raw": 63,
  "moisture_percent": 61.67,
  "ph_raw": 50,
  "ph_voltage": 0.04,
  "ph": 14,
  "uptime": 123
}
```

## Lab Output

During the final lab run, the ESP32 initialized the sensors, connected to WiFi, published readings over MQTT, and wrote to Firebase.

```txt
DHT22 initialized on GPIO 4
Soil moisture sensor initialized on GPIO 32
PH-4502C sensor initialized on GPIO 33
Connecting to WiFi...
WiFi status: 1000
WiFi status: 1000
WiFi connected
MQTT connected
MQTT published
Firebase published: 200
```

The cleaned lab readings were saved in:

- `data/readings.txt` for the readable serial-monitor log.
- `data/firebase-readings.json` for Firebase-ready structured readings.

## Data Collected

We collected 29 cleaned sensor readings. Each JSON reading included the bed ID, device name, DHT sensor type, temperature, humidity, moisture raw value, moisture percentage, pH raw value, pH voltage, calculated pH, MQTT status, Firebase status, and overall status.

The JSON file was prepared so it could be uploaded directly to Firebase Realtime Database and later fetched by the dashboard.

## Dashboard

The dashboard is a single static page in `dashboard/`. It currently fetches the local `data/firebase-readings.json` file every 5 seconds and plays the readings from `reading_001` through `reading_029` so the page feels like live incoming sensor data during demos.

Start the local Python server from the project root:

```powershell
python -m http.server 8080 --bind 127.0.0.1
```

Then open:

```txt
http://127.0.0.1:8080/dashboard/
```

If port `8080` is already in use, choose another port:

```powershell
python -m http.server 8081 --bind 127.0.0.1
```

The dashboard is designed so the local fetch can later be replaced with a Firestore fetch that runs every 5 seconds. For Firestore integration, we will add the Firebase web SDK, configure the Firebase app, read from a `readings` collection ordered by timestamp or reading number, and pass those documents into the same dashboard rendering function.

## Calibration Values

The analog conversion and offsets used by the firmware were stored in `esp32/config.py`.

```python
MOISTURE_DRY_RAW = 100
MOISTURE_WET_RAW = 40

DHT_TEMP_OFFSET = -5.0
DHT_HUM_OFFSET = 20.0

PH_NEUTRAL_VOLTAGE = 2.5
PH_SLOPE = -5.7

ADC_MAX_VALUE = 4095
ADC_REFERENCE_VOLTAGE = 3.3
```

These values helped convert raw ADC readings into percentages and pH estimates for display, MQTT publishing, and Firebase storage.

## Project Outcome

We completed the sensor-to-cloud pipeline for the IoT vermiculture monitoring project. The ESP32 read the physical sensors, displayed results locally, connected to WiFi, published MQTT messages, and stored readings in Firebase. The cleaned dataset was also prepared for the dashboard phase.
