# ESP32 Pin Mapping

## Current Prototype Components

* ESP32 development board
* DHT22 temperature and humidity sensor
* Soil moisture sensor
* pH-4502C pH sensor
* SSD1306 OLED display
* 4.5kΩ resistor
* Breadboard
* Jumper wires

## Pin Assignment

| Component            | Signal Pin | ESP32 Pin | Notes                                  |
| -------------------- | ---------: | --------: | -------------------------------------- |
| DHT22                |       DATA |    GPIO21 | Measures both temperature and humidity |
| Soil Moisture Sensor |       AOUT |    GPIO36 | Analog input, ADC1                     |
| pH-4502C             |         Po |    GPIO35 | Analog input, ADC1                     |
| OLED Display         |        SDA |    GPIO22 | I2C data                               |
| OLED Display         |        SCL |    GPIO23 | I2C clock                              |

## Power Connections

| Component            | VCC      | GND |
| -------------------- | -------- | --- |
| DHT22                | 3.3V     | GND |
| Soil Moisture Sensor | 3.3V     | GND |
| OLED Display         | 3.3V     | GND |
| pH-4502C             | VIN / 5V | GND |

## Resistor Usage

One 4.5kΩ resistor is used as a pull-up resistor for the DHT22 data line.

Connection:

```txt
ESP32 3.3V ---- 4.5kΩ resistor ---- DHT22 DATA ---- ESP32 GPIO21
```

The DHT22 commonly uses a 10kΩ pull-up resistor, but the available 4.5kΩ resistor can work for a short lab prototype. If the DHT22 is a 3-pin module, it may already include a pull-up resistor, so the external resistor may not be required.

## Full Wiring Summary

```txt
DHT22 VCC          -> ESP32 3.3V
DHT22 GND          -> ESP32 GND
DHT22 DATA         -> ESP32 GPIO21
4.5kΩ resistor     -> between DHT22 DATA and ESP32 3.3V

Soil Moisture VCC  -> ESP32 3.3V
Soil Moisture GND  -> ESP32 GND
Soil Moisture AOUT -> ESP32 GPIO36

pH-4502C V+        -> ESP32 VIN / 5V
pH-4502C GND       -> ESP32 GND
pH-4502C Po        -> ESP32 GPIO35

OLED VCC           -> ESP32 3.3V
OLED GND           -> ESP32 GND
OLED SDA           -> ESP32 GPIO22
OLED SCL           -> ESP32 GPIO23
```

## Important Notes

All sensor grounds must connect to the same ESP32 GND. A common ground is required for stable analog readings.

GPIO35 and GPIO36 are ADC1 pins, so they are suitable for analog sensor readings while Wi-Fi is active.

The ESP32 GPIO pins are 3.3V tolerant only. The pH-4502C analog output must be checked with a multimeter before connecting it to GPIO35 in the physical circuit. The output should remain within 0V to 3.3V.

The DHT22 is used as the only temperature and humidity sensor in this prototype, following the lab implementation instruction.
