# ESP32 Pin Mapping

## Current Prototype Components

* ESP32 development board
* DHT22 temperature and humidity sensor
* Soil moisture sensor
* pH-4502C pH sensor
* SSD1306 OLED display
* 1 × 10kΩ resistor
* Breadboard
* Jumper wires
* USB power supply + USB-C to micro-USB cable

## Pin Assignment

| Component            | Sensor Pin | ESP32 Pin | Notes                                  |
| -------------------- | ---------: | --------: | -------------------------------------- |
| DHT22                |       DATA |    GPIO21 | Digital input; temp + air humidity     |
| Soil Moisture Sensor |       AOUT |    GPIO33 | Analog input, ADC1                       |
| pH-4502C             |         Po |    GPIO35 | Analog input, ADC1                       |
| OLED Display         |        SDA |    GPIO22 | I2C data                               |
| OLED Display         |        SCL |    GPIO23 | I2C clock                              |

## Power Connections

Power the ESP32 from USB. Use the ESP32 board pins below — do not feed 5V into any sensor signal pin.

| Component            | Sensor Pin | Connect To (ESP32 Board Pin) |
| -------------------- | ---------- | ------------------------------ |
| DHT22                | VCC        | **3V3**                        |
| DHT22                | GND        | **GND**                        |
| Soil Moisture Sensor | VCC        | **3V3**                        |
| Soil Moisture Sensor | GND        | **GND**                        |
| OLED Display         | VCC        | **3V3**                        |
| OLED Display         | GND        | **GND**                        |
| pH-4502C             | V+         | **VIN** (5V from USB)          |
| pH-4502C             | GND        | **GND**                        |

### Power Rail Summary

```txt
USB power supply
    └── USB cable ──► ESP32 USB port
                          │
                          ├── 3V3 pin ──┬── DHT22 VCC
                          │             ├── Soil Moisture VCC
                          │             └── OLED VCC
                          │
                          ├── VIN pin ────── pH-4502C V+
                          │
                          └── GND pin ──┬── DHT22 GND
                                        ├── Soil Moisture GND
                                        ├── OLED GND
                                        └── pH-4502C GND
```

All grounds must share one common GND rail on the breadboard, tied back to the ESP32 **GND** pin.

## Resistor Usage

One **10kΩ** resistor is used as the pull-up on the DHT22 data line.

Connection:

```txt
ESP32 3V3 ──── 10kΩ resistor ──── DHT22 DATA ──── ESP32 GPIO21
```

If the DHT22 is a 3-pin module with a built-in pull-up resistor, you may omit the external 10kΩ resistor. For a bare 4-pin DHT22, the external 10kΩ resistor is required.

## Full Wiring Summary

### Signal connections

```txt
DHT22 DATA         -> ESP32 GPIO21
Soil Moisture AOUT -> ESP32 GPIO33
pH-4502C Po        -> ESP32 GPIO35
OLED SDA           -> ESP32 GPIO22
OLED SCL           -> ESP32 GPIO23
```

### Power connections

```txt
DHT22 VCC              -> ESP32 3V3
DHT22 GND              -> ESP32 GND
Soil Moisture VCC      -> ESP32 3V3
Soil Moisture GND      -> ESP32 GND
pH-4502C V+            -> ESP32 VIN (5V)
pH-4502C GND           -> ESP32 GND
OLED VCC               -> ESP32 3V3
OLED GND               -> ESP32 GND
10kΩ resistor          -> between DHT22 DATA and ESP32 3V3
```

## Complete Connection Table

| From (Component.Pin)   | To (ESP32 Board Pin) |
| ---------------------- | -------------------- |
| DHT22.VCC              | 3V3                  |
| DHT22.GND              | GND                  |
| DHT22.DATA             | GPIO21               |
| DHT22.DATA             | 3V3 (via 10kΩ)       |
| Soil Moisture.VCC      | 3V3                  |
| Soil Moisture.GND      | GND                  |
| Soil Moisture.AOUT     | GPIO33               |
| pH-4502C.V+            | VIN                  |
| pH-4502C.GND           | GND                  |
| pH-4502C.Po            | GPIO35               |
| OLED.VCC               | 3V3                  |
| OLED.GND               | GND                  |
| OLED.SDA               | GPIO22               |
| OLED.SCL               | GPIO23               |

## Important Notes

* All sensor grounds must connect to the same ESP32 **GND**. A common ground is required for stable analog readings.
* **GPIO33** and **GPIO35** are ADC1 pins, so they are safe for analog sensor readings while Wi-Fi is active.
* GPIO36 is not available on this ESP32 board variant, so soil moisture uses **GPIO33** instead.
* ESP32 GPIO pins are **3.3V tolerant only**. Before connecting pH-4502C **Po** to GPIO35, tune the module potentiometer and confirm with a multimeter that the output stays within **0V–3.3V** (about 1.65V at pH 7).
* The DHT22 is the only temperature and humidity sensor in this prototype, per lab instructions. Bed moisture comes from the dedicated soil moisture sensor on GPIO33.
