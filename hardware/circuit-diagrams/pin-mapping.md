# ESP32 Pin Mapping

## Current Prototype Components

- ESP32 development board
- OLED display, 1.30" IIC v2.2, using SH1106-style I2C driver in MicroPython
- DHT11 temperature and humidity sensor
- DHT22 temperature and humidity sensor
- Soil moisture sensor
- pH-4502C pH sensor module
- 1 x 10k ohm resistor
- Breadboard
- Jumper wires
- USB power supply / USB cable

## Current Code Structure

The ESP32 firmware is split into separate MicroPython files:

```txt
esp32/
  main.py
  config.py
  sh1106.py
  oled_display.py
  sensors.py
  wifi_manager.py
  mqtt_manager.py
  firebase_client.py
```

The active pin mapping is controlled from `config.py`.

Current cloud settings during hardware testing:

```python
USE_WIFI = False
USE_MQTT = False
USE_FIREBASE = False
```

This means the ESP32 will not try to connect to WiFi, MQTT, or Firebase yet. It will only test the OLED, selected DHT sensor, soil moisture sensor, and pH sensor locally.

## Current Pin Assignment

This mapping matches the current code setup before final pin remapping.

| Component | Sensor Pin | ESP32 Pin | Notes |
|---|---:|---:|---|
| Selected DHT sensor | DATA | GPIO4 | Digital input; controlled by `DHT_SENSOR_TYPE` in `config.py` |
| Soil moisture sensor | AOUT | GPIO34 | Analog input, ADC1 |
| pH-4502C | Po | GPIO35 | Analog input, ADC1 |
| OLED display | SDA | GPIO21 | I2C data |
| OLED display | SCL | GPIO22 | I2C clock |

Current `config.py` pin values:

```python
OLED_SDA = 21
OLED_SCL = 22
DHT_PIN = 4
MOISTURE_PIN = 34
PH_PIN = 35
```

## DHT11 / DHT22 Selection

The code is written to use either DHT11 or DHT22, not both at the same time.

Even if both sensors are available physically, the firmware reads only the sensor selected in `config.py`.

To test DHT11:

```python
DHT_SENSOR_TYPE = "DHT11"
DHT_PIN = 4
```

To test DHT22:

```python
DHT_SENSOR_TYPE = "DHT22"
DHT_PIN = 4
```

The selected sensor's DATA pin must be connected to GPIO4.

Do not connect both DHT11 DATA and DHT22 DATA to GPIO4 at the same time. Test one sensor at a time unless the code is later changed to support two separate DHT pins.

## Power Connections

Power the ESP32 from USB. Use the ESP32 board power pins. Do not feed 5V into any ESP32 GPIO signal pin.

| Component | Sensor Pin | Connect To |
|---|---:|---:|
| DHT11 or DHT22 | VCC | ESP32 3V3 |
| DHT11 or DHT22 | GND | ESP32 GND |
| Soil moisture sensor | VCC | ESP32 3V3 |
| Soil moisture sensor | GND | ESP32 GND |
| OLED display | VCC | ESP32 3V3 |
| OLED display | GND | ESP32 GND |
| pH-4502C | V+ | ESP32 VIN / 5V |
| pH-4502C | GND | ESP32 GND |

Power rail summary:

```txt
USB power supply
  -> USB cable -> ESP32 USB port
       -> 3V3 pin -> DHT11/DHT22 VCC
       -> 3V3 pin -> Soil moisture VCC
       -> 3V3 pin -> OLED VCC
       -> VIN pin -> pH-4502C V+
       -> GND pin -> common breadboard GND rail
```

All grounds must share one common GND rail on the breadboard, tied back to the ESP32 GND pin.

## Resistor Usage

The 10k ohm resistor is used as a pull-up resistor for the selected DHT sensor data line.

Connection:

```txt
ESP32 3V3 -> 10k ohm resistor -> DHT DATA -> ESP32 GPIO4
```

For DHT11:

```txt
ESP32 3V3 -> 10k ohm resistor -> DHT11 DATA -> ESP32 GPIO4
```

For DHT22:

```txt
ESP32 3V3 -> 10k ohm resistor -> DHT22 DATA -> ESP32 GPIO4
```

If the DHT sensor is a 3-pin module with a built-in pull-up resistor, the external 10k ohm resistor may not be required. If it is a bare 4-pin DHT sensor, the external resistor should be used.

## Full Wiring Summary

Signal connections:

```txt
Selected DHT DATA  -> ESP32 GPIO4
Soil moisture AOUT -> ESP32 GPIO34
pH-4502C Po        -> ESP32 GPIO35
OLED SDA           -> ESP32 GPIO21
OLED SCL           -> ESP32 GPIO22
```

Power connections:

```txt
DHT11/DHT22 VCC   -> ESP32 3V3
DHT11/DHT22 GND   -> ESP32 GND
Soil moisture VCC -> ESP32 3V3
Soil moisture GND -> ESP32 GND
pH-4502C V+       -> ESP32 VIN / 5V
pH-4502C GND      -> ESP32 GND
OLED VCC          -> ESP32 3V3
OLED GND          -> ESP32 GND
10k ohm resistor  -> between selected DHT DATA and ESP32 3V3
```

Complete connection table:

| From | To |
|---|---|
| DHT11/DHT22 VCC | ESP32 3V3 |
| DHT11/DHT22 GND | ESP32 GND |
| DHT11/DHT22 DATA | ESP32 GPIO4 |
| DHT11/DHT22 DATA | ESP32 3V3 via 10k ohm resistor |
| Soil moisture VCC | ESP32 3V3 |
| Soil moisture GND | ESP32 GND |
| Soil moisture AOUT | ESP32 GPIO34 |
| pH-4502C V+ | ESP32 VIN / 5V |
| pH-4502C GND | ESP32 GND |
| pH-4502C Po | ESP32 GPIO35 |
| OLED VCC | ESP32 3V3 |
| OLED GND | ESP32 GND |
| OLED SDA | ESP32 GPIO21 |
| OLED SCL | ESP32 GPIO22 |

## Important Notes

- The OLED is being handled using an SH1106-style driver, not the standard SSD1306 driver. This matches many 1.30" IIC OLED modules.
- The OLED must appear during I2C scanning. A successful scan usually shows address `0x3C`, printed as `[60]` in MicroPython.
- If the scan shows `[]`, the OLED is not being detected. Check SDA, SCL, VCC, GND, breadboard contact, and OLED module condition.
- GPIO34 and GPIO35 are ADC1 pins, so they are suitable for analog readings while WiFi is active.
- GPIO34 and GPIO35 are input-only pins. That is fine for soil moisture and pH analog readings.
- ESP32 GPIO pins are 3.3V tolerant only. Before connecting pH-4502C Po to GPIO35, confirm that the output stays within 0V to 3.3V.
- The pH-4502C module may be powered from VIN / 5V, but its analog output going into the ESP32 must still be safe for 3.3V logic.
- All grounds must be common. The ESP32, DHT sensor, OLED, soil moisture sensor, and pH module must share GND.
- The current firmware reads either DHT11 or DHT22 based on `DHT_SENSOR_TYPE`. It does not read both DHT sensors simultaneously.
