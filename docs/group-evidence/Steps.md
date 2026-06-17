# Implementation and Testing Evidence

This file summarizes the screenshots and photos captured during the project. These images can be used in the final report to prove the setup, testing, debugging, and final data upload process.

## 1. Python and ESP32 Tool Setup

We first set up a Python virtual environment and installed `esptool`, which was used to communicate with the ESP32 and install MicroPython firmware.

Commands used:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install esptool
python -m esptool version
```

## 2. ESP32 Detection and Communication

### 1a. ESP32 detected on the laptop

Screenshot:
`screenshots/1a.ESP32-detected-on-device-manager.png`

This screenshot shows that the ESP32 was detected by the laptop through Device Manager. This confirmed that the board was connected and visible through a COM port.

### 1b. ESP32 communication error and fix

Screenshot:
`screenshots/1b.ESP32-communication-error-and-fix.png`

Command used:

```powershell
python -m esptool --chip esp32 --port COM8 --baud 115200 chip_id
```

The command first failed because the COM8 port was busy. We fixed this by closing programs that were using the port, including Thonny IDE and Device Manager. After that, the ESP32 could communicate with the laptop.

## 3. Flashing MicroPython Firmware

### 2a. Erasing ESP32 flash memory

Screenshot:
`screenshots/2a.Erasing-ESP32-flash-memory.png`

Command used:

```powershell
cd .\firmware\physical\
python -m esptool --chip esp32 --port COM8 --baud 115200 erase_flash
```

This step cleared the existing firmware from the ESP32 before installing MicroPython.

### 2b. Installing new MicroPython firmware

Screenshot:
`screenshots/2b.Installing-new-firmware.png`

Command used:

```powershell
python -m esptool --chip esp32 --port COM8 --baud 460800 write_flash -z 0x1000 ESP32_GENERIC.bin
```

The MicroPython firmware file was stored in `firmware/physical`. After flashing, the ESP32 was ready to run the project Python files.

## 4. Wokwi Prototype

Image:
`8.Wokwi-implementation.png`

We used Wokwi to prototype the circuit before wiring the physical components. The Wokwi implementation helped us plan how the ESP32, DHT22, OLED display, and analog inputs would work together.

In the Wokwi simulation, potentiometers were used to represent analog sensors:

- One potentiometer represents the pH sensor output.
- The other potentiometer represents the soil moisture sensor output.

Turning the potentiometers simulates changing analog values, similar to how the real pH and moisture sensors produce different readings.

## 5. OLED Display Testing

### 3a. OLED test error

Screenshot:
`screenshots/3a.OLED-test-error.png`

The OLED display was added so the ESP32 could show readings locally. During testing, the ESP32 ran the OLED driver code, but the I2C scan returned abnormal results instead of detecting the expected SH1106 OLED address.

### 3b. OLED test fix

Screenshot:
`screenshots/3b.OLED-test-fix.png`

The problem was caused by wiring. After correcting the OLED wiring, the display was detected properly through I2C scanning. The OLED display code is handled in `esp32/oled_display.py`.

## 6. Sensor Testing

### 4a. DHT22 sensor error

Screenshot:
`screenshots/4a.DHT22-sensor-error.png`

After connecting the full circuit, including the pH sensor, DHT22, and soil moisture sensor, the DHT22 readings were not detected correctly.

### 4b. DHT22 sensor fix

Screenshot:
`screenshots/4b.DHT22-sensor-fix.png`

The issue was caused by a physical connection problem. After fixing the wiring, the ESP32 was able to read sensor values correctly. Sensor reading logic is handled in `esp32/sensors.py`.

Physical circuit photo:
`Physical-circuit photo.jpeg`

This image can be used to show the final breadboard setup.

## 7. WiFi Testing

### 5a. WiFi error

Screenshot:
`screenshots/5a.Wifi-error.png`

The ESP32 initially failed to connect to WiFi.

### 5b. WiFi error fix

Screenshot:
`screenshots/5b.Wifi-error-fix.png`

The issue was caused by an incorrect IP/configuration value. After correcting the configuration, the ESP32 connected successfully. WiFi connection logic is handled in `esp32/wifi_manager.py`, while the configuration values are stored in `esp32/config.py`.

## 8. MQTT Testing

### 6. MQTT publishing and subscribing

Screenshot:
`screenshots/6.MQTT-publishing&subscribing.png`

We used a local Mosquitto broker to test MQTT publishing and subscribing.

Local Mosquitto configuration:

```txt
listener 1883 0.0.0.0
allow_anonymous true
```

Broker command:

```powershell
& "C:\Program Files\mosquitto\mosquitto.exe" -c "C:\Users\emman\Development\Group2-IOT-Semester-Project\mosquitto-local.conf" -v
```

The broker first failed until it was run with administrator permissions.

Subscriber command:

```powershell
& "C:\Program Files\mosquitto\mosquitto_sub.exe" -h 127.0.0.1 -p 1883 -t "iot/group2/project" -v
```

This confirmed that messages published by the ESP32 could be received by the local computer. MQTT publishing is handled in `esp32/mqtt_manager.py`.

## 9. Firebase Publishing

### 7a. Firebase publishing success

Screenshot:
`screenshots/7a.Firebase-publishing-success.png`

This screenshot shows that the ESP32 successfully uploaded readings to Firebase.

### 7b. Realtime Database readings

Screenshot:
`screenshots/7b.RealtimeDatabase-readings.jpeg`

This shows readings stored in Firebase Realtime Database.

### 7c. Firestore database readings

Screenshot:
`screenshots/7c.FirestoreDatabase-readings.png`

This can be used as additional database evidence if the final report discusses Firestore storage or imported readings.

Firebase upload logic is handled in `esp32/firebase_client.py`.

## 10. Data and Dashboard Evidence

The cleaned readings were saved in:

- `data/readings.txt` - readable serial-monitor output.
- `data/firebase-readings.json` - structured JSON readings for Firebase/dashboard demonstration.

The dashboard files are stored in:

- `dashboard/`

The dashboard uses the cleaned Firebase-ready JSON readings to demonstrate how the collected sensor data can be visualized.

## 11. Group Evidence

Image:
`Group2-photo.jpeg`

This image can be used in the appendix as group participation evidence.
