# Updated IoT Project Roadmap

## Current Implementation Direction

The project is being implemented using MicroPython on an ESP32 with a split-file firmware structure.

The current firmware is based on another group's working code, but it has been reorganized into separate files for easier testing and debugging. The system currently includes an ESP32, OLED display, selected DHT sensor, soil moisture sensor, pH-4502C sensor, and a 10k ohm DHT pull-up resistor.

The testing strategy is staged. Local hardware readings should work first, then WiFi, then pin remapping, then MQTT and Firebase.

## Current Firmware Files

```txt
main.py              -> main program loop
config.py            -> WiFi, MQTT, Firebase, pins, calibration values
sh1106.py            -> OLED driver
oled_display.py      -> OLED setup and display helper functions
sensors.py           -> DHT, soil moisture, and pH read functions
wifi_manager.py      -> WiFi connection logic
mqtt_manager.py      -> MQTT connection and publishing logic
firebase_client.py   -> Firebase upload logic
```

## Stage 1 - Code Split and Configuration

Status: in progress / mostly done.

Tasks:

- Create separate MicroPython files.
- Move pin settings into `config.py`.
- Move sensor logic into `sensors.py`.
- Move OLED logic into `oled_display.py` and `sh1106.py`.
- Move WiFi logic into `wifi_manager.py`.
- Move MQTT logic into `mqtt_manager.py`.
- Move Firebase logic into `firebase_client.py`.
- Keep `USE_WIFI = False`.
- Keep `USE_MQTT = False`.
- Keep `USE_FIREBASE = False`.

Expected result:

- Code uploads cleanly to the ESP32.
- `main.py` imports all files correctly.
- There are no missing module errors.
- There are no WiFi, MQTT, or Firebase connection attempts yet.

## Stage 2 - WiFi Setup Check

Status: next after code files are stable.

Even though cloud features remain off during sensor testing, WiFi credentials should be prepared in `config.py`.

Current settings:

```python
WIFI_SSID = "K8597"
WIFI_PASSWORD = "00001111"
```

For WiFi-only testing, temporarily set:

```python
USE_WIFI = True
USE_MQTT = False
USE_FIREBASE = False
```

Tasks:

- Confirm the hotspot/router is on.
- Confirm the ESP32 can connect to WiFi.
- Check the IP address in Thonny output.
- Keep Firebase off.
- Do not publish sensor readings yet.

Expected result:

- WiFi connects.
- IP address prints in Thonny.
- OLED shows a WiFi connected message.

## Stage 3 - Pin Remapping

Status: next after WiFi setup is confirmed.

Reason for remapping:

- Avoid copying the other group's exact pin layout.
- Use ADC1 pins for analog sensors.
- Keep I2C pins stable for OLED testing.
- Keep DHT on a reliable digital GPIO.

Current pin setup before remapping:

```python
OLED_SDA = 21
OLED_SCL = 22
DHT_PIN = 4
MOISTURE_PIN = 34
PH_PIN = 35
```

Possible remapped setup to use later:

```python
OLED_SDA = 18
OLED_SCL = 19
DHT_PIN = 27
MOISTURE_PIN = 32
PH_PIN = 33
```

Do not apply this remap until the current setup has been tested first.

## Stage 4 - Local Hardware Testing

Status: immediate practical testing stage.

Cloud settings must remain:

```python
USE_WIFI = False
USE_MQTT = False
USE_FIREBASE = False
```

Testing order:

1. Test OLED detection using I2C scan.
2. Test the selected DHT sensor.
3. Test soil moisture raw ADC reading.
4. Test pH raw ADC reading.
5. Display all readings on OLED.
6. Print all readings in Thonny.

Expected output:

```txt
I2C scan: [60]
DHT11 or DHT22 initialized on GPIO4
Soil moisture sensor initialized on GPIO34
PH-4502C sensor initialized on GPIO35
Temperature and humidity printed
Moisture raw value printed
pH raw value and voltage printed
OLED displays readings
```

If the OLED scan shows `I2C scan: []`, the OLED is not detected. Fix OLED wiring before debugging MQTT or Firebase.

If DHT readings return `DHT read error`, check DHT wiring, sensor type in `config.py`, DATA pin, and pull-up resistor.

## Stage 5 - MQTT Publishing

Status: after local readings and WiFi work.

Turn MQTT on:

```python
USE_WIFI = True
USE_MQTT = True
USE_FIREBASE = False
```

Tasks:

- Confirm WiFi connects.
- Confirm MQTT broker address is correct.
- Confirm MQTT topic is correct.
- Publish JSON payload from ESP32.
- Subscribe from laptop or backend to verify message arrival.

Current placeholder MQTT settings:

```python
MQTT_BROKER = "192.168.137.89"
MQTT_PORT = 1883
MQTT_TOPIC = "iot/lab/sensor"
```

Possible group topic:

```python
MQTT_TOPIC = "iot/lab/group4e/vermiculture"
```

Expected result:

- ESP32 connects to WiFi.
- ESP32 connects to the MQTT broker.
- `MQTT published` prints.
- Subscriber receives JSON readings.

## Stage 6 - Firebase Setup

Status: last cloud stage.

Firebase should stay off until MQTT and local readings are stable.

Turn Firebase on only when ready:

```python
USE_WIFI = True
USE_MQTT = True
USE_FIREBASE = True
```

Or, for Firebase-only testing:

```python
USE_WIFI = True
USE_MQTT = False
USE_FIREBASE = True
```

Tasks:

- Confirm Firebase Realtime Database URL.
- Confirm URL ends with `.json`.
- Confirm ESP32 has internet access.
- Confirm `urequests` is available.
- Send latest readings using `PUT`.
- Close response using `response.close()`.
- Check Firebase database for saved reading.

Important Firebase note:

```python
response.close()
```

The other group's original code had a broken line:

```python
res.clo    se()
```

That must never be used. It will crash.

## Stage 7 - Backend / Dashboard Direction

The older roadmap described MQTT, a Node.js/Express backend, MongoDB Atlas, and a React dashboard. That direction is still valid as a full system architecture, but for the immediate lab stage, the priority is sensor data collection first.

Updated practical order:

1. ESP32 local readings.
2. OLED display.
3. WiFi connection.
4. Pin remapping.
5. MQTT publishing.
6. Firebase latest-reading backup.
7. Optional backend/dashboard.
8. Documentation and demo evidence.

For the current working version, Firebase can act as a simple cloud database for readings. A full backend and dashboard can come after the ESP32 data flow is stable.

## Immediate Next Steps

1. Keep `USE_WIFI = False`.
2. Keep `USE_MQTT = False`.
3. Keep `USE_FIREBASE = False`.
4. Upload all MicroPython files to ESP32.
5. Run `main.py`.
6. Confirm OLED scan.
7. Confirm selected DHT sensor reading.
8. Confirm soil moisture raw reading.
9. Confirm pH raw and voltage reading.
10. Only after this, test WiFi using `USE_WIFI = True`.
11. After WiFi works, remap pins.
12. After remapped local readings work, enable MQTT.
13. After MQTT works, enable Firebase.
