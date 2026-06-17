# ESP32 Final Pin Remapping Plan

## Purpose

This remapping gives the project a clean pin layout while still using sensible ESP32 pins.

The current hardware has already been proven to work using the original pins. Apply this remap only after the split code works with the current setup.

## Current Working Pins

These are the pins used while proving the sensors and OLED work:

| Component | Signal | Current ESP32 Pin | Notes |
|---|---:|---:|---|
| OLED display | SDA | GPIO21 | I2C data |
| OLED display | SCL | GPIO22 | I2C clock |
| DHT22 | DATA | GPIO4 | Temperature and humidity |
| Soil moisture sensor | AOUT | GPIO34 | Analog input, ADC1 |
| pH-4502C | Po | GPIO35 | Analog input, ADC1 |

## Final Remapped Pins

Use this final mapping for our group:

| Component | Signal | New ESP32 Pin | Reason |
|---|---:|---:|---|
| OLED display | SDA | GPIO18 | Alternate I2C data pin |
| OLED display | SCL | GPIO19 | Alternate I2C clock pin |
| DHT22 | DATA | GPIO27 | Reliable digital GPIO for DHT data |
| Soil moisture sensor | AOUT | GPIO32 | ADC1 analog input, works while WiFi is active |
| pH-4502C | Po | GPIO33 | ADC1 analog input, works while WiFi is active |

## Final `config.py` Values

Update the pin section in `esp32/config.py` to:

```python
OLED_SDA = 18
OLED_SCL = 19

DHT_PIN = 4

MOISTURE_PIN = 32
PH_PIN = 33
```

Keep the DHT sensor type as:

```python
DHT_SENSOR_TYPE = "DHT22"
```

## Physical Wiring After Remapping

After changing the software pins, rewire the hardware to match:

| Sensor / Module | Module Pin | ESP32 Pin |
|---|---:|---:|
| OLED display | SDA | GPIO18 |
| OLED display | SCL | GPIO19 |
| DHT22 | DATA | GPIO27 |
| Soil moisture sensor | AOUT | GPIO32 |
| pH-4502C | Po | GPIO33 |

Power connections stay the same:

| Sensor / Module | Module Pin | ESP32 Pin |
|---|---:|---:|
| OLED display | VCC | 3V3 |
| OLED display | GND | GND |
| DHT22 | VCC | 3V3 |
| DHT22 | GND | GND |
| Soil moisture sensor | VCC | 3V3 |
| Soil moisture sensor | GND | GND |
| pH-4502C | V+ | VIN / 5V |
| pH-4502C | GND | GND |

The 10k ohm pull-up resistor should remain between DHT22 DATA and 3V3:

```txt
ESP32 3V3 -> 10k ohm resistor -> DHT22 DATA -> ESP32 GPIO27
```

## Testing Order

1. Change the pin values in `esp32/config.py`.
2. Upload the split code files to the ESP32.
3. Rewire OLED SDA/SCL to GPIO18/GPIO19.
4. Rewire DHT22 DATA to GPIO27.
5. Rewire soil moisture AOUT to GPIO32.
6. Rewire pH-4502C Po to GPIO33.
7. Run `main_split_test.py` from Thonny.
8. Confirm the OLED scan still shows `[60]`.
9. Confirm DHT22 temperature and humidity readings.
10. Confirm soil moisture raw and percentage readings.
11. Confirm pH raw, voltage, and pH value readings.

## Notes

- GPIO32 and GPIO33 are ADC1 pins, so they are suitable for analog readings while WiFi is active.
- GPIO34 and GPIO35 also work for analog input, but GPIO32 and GPIO33 keep the final layout consistent with the firmware.
- GPIO27 is a good normal digital GPIO for the DHT22 data line.
- GPIO18 and GPIO19 can be used for I2C in MicroPython because the code creates the I2C bus with explicit SDA and SCL pins.
- Do not move to WiFi, MQTT, or Firebase until the remapped local readings are stable.
