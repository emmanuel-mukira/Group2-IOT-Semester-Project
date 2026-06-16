# ESP32 Pin Mapping

## Current Prototype Components

* ESP32 development board
* DS18B20 waterproof temperature sensor
* DHT22 ambient temperature and humidity sensor
* Soil moisture sensor
* pH-4502C pH sensor
* SSD1306 OLED display
* 4.5kΩ resistor
* Breadboard
* Jumper wires

## Pin Assignment

| Component            | Signal Pin | ESP32 Pin | Notes                               |
| -------------------- | ---------: | --------: | ----------------------------------- |
| DS18B20              |  DQ / DATA |     GPIO4 | Uses 4.5kΩ pull-up resistor to 3.3V |
| DHT22                |       DATA |    GPIO21 | Ambient temperature and humidity    |
| Soil Moisture Sensor |       AOUT |    GPIO36 | Analog input, ADC1                  |
| pH-4502C             |         Po |    GPIO35 | Analog input, ADC1                  |
| OLED Display         |        SDA |    GPIO22 | I2C data                            |
| OLED Display         |        SCL |    GPIO23 | I2C clock                           |

## Power Connections

| Component            | VCC      | GND |
| -------------------- | -------- | --- |
| DS18B20              | 3.3V     | GND |
| DHT22                | 3.3V     | GND |
| Soil Moisture Sensor | 3.3V     | GND |
| OLED Display         | 3.3V     | GND |
| pH-4502C             | VIN / 5V | GND |

## Resistor Usage

One 4.5kΩ resistor is used as a pull-up resistor for the DS18B20 data line.

Connection:

```txt
ESP32 3.3V ---- 4.5kΩ resistor ---- DS18B20 DQ/DATA ---- ESP32 GPIO4
```

The DS18B20 normally uses a 4.7kΩ pull-up resistor, so the available 4.5kΩ resistor is close enough for this prototype.

## Full Wiring Summary

```txt
DS18B20 VCC       -> ESP32 3.3V
DS18B20 GND       -> ESP32 GND
DS18B20 DQ/DATA   -> ESP32 GPIO4
4.5kΩ resistor    -> between DS18B20 DATA and ESP32 3.3V

DHT22 VCC         -> ESP32 3.3V
DHT22 GND         -> ESP32 GND
DHT22 DATA        -> ESP32 GPIO21

Soil Moisture VCC -> ESP32 3.3V
Soil Moisture GND -> ESP32 GND
Soil Moisture AOUT-> ESP32 GPIO36

pH-4502C V+       -> ESP32 VIN / 5V
pH-4502C GND      -> ESP32 GND
pH-4502C Po       -> ESP32 GPIO35

OLED VCC          -> ESP32 3.3V
OLED GND          -> ESP32 GND
OLED SDA          -> ESP32 GPIO22
OLED SCL          -> ESP32 GPIO23
```

## Important Notes

All sensor grounds must connect to the same ESP32 GND. This common ground is required for stable analog readings.

GPIO35 and GPIO36 are ADC1 pins, so they are suitable for analog sensor readings while Wi-Fi is active.

The ESP32 GPIO pins are 3.3V tolerant only. The pH-4502C analog output must be checked with a multimeter before connecting it to GPIO35 in the physical circuit. The output should remain within 0V to 3.3V.

The DHT22 is used for ambient air temperature and humidity, while the DS18B20 is used for internal vermiculture bed temperature.
