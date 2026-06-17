SIMPLE DOCUMENTATION ROADMAP

Use this as the structure for the final project report. Keep the writing simple and focus on what was actually built.

FRONT MATTER
Cover page - university name, unit code ICS 4111, project title, Group 2, member names and student IDs, and submission date.
Table of contents.
List of figures and tables, if required.

SECTION 1 - INTRODUCTION
Briefly explain:
What vermiculture is.
Who the system is meant to help.
Why monitoring temperature, humidity, soil moisture, and pH is useful.
The problem with checking beds manually.

Keep this section short. Do not over-explain the whole organic farming industry.

SECTION 2 - OBJECTIVES AND SCOPE
Main objective:
To design and prototype an IoT system for monitoring vermiculture bed conditions.

Specific objectives:
Read temperature and humidity using a DHT22 sensor.
Read soil moisture using an analog moisture sensor.
Read pH using a PH-4502C sensor.
Display readings on an OLED screen.
Send readings using MQTT.
Upload readings to Firebase.
Show the collected readings on a dashboard.

Scope:
This is a prototype monitoring and data-logging system. It does not automate irrigation, control shade, send SMS alerts, or predict harvest readiness.

SECTION 3 - BACKGROUND
Keep this section simple. Cover only:
Basic vermiculture conditions: temperature, moisture, humidity, and pH.
How IoT helps in agriculture.
Why MQTT is useful for sending small sensor readings.
Why Firebase is suitable for storing simple JSON readings in this prototype.

SECTION 4 - METHODOLOGY AND IMPLEMENTATION
This section should explain both the hardware and software steps in the order the project was built.

4.1 System overview
Add a simple diagram showing:
Sensors -> ESP32 -> OLED display -> MQTT/Firebase -> Dashboard.

Explain that the ESP32 collects sensor values, displays them locally, sends them through MQTT, uploads them to Firebase, and the dashboard visualizes saved readings.

4.2 Wokwi simulation/prototype
Explain that Wokwi was used first to plan and test the circuit idea before physical wiring.

Use this image here:
docs/group-evidence/Wokwi-implementation.png

Important explanation:
In the Wokwi simulation, potentiometers were used to represent analog sensors. One potentiometer represents the pH sensor output, and the other potentiometer represents the soil moisture sensor output. Turning the potentiometers simulates changing analog readings.

4.3 Hardware setup
List the hardware used:
ESP32 development board.
DHT22 temperature and humidity sensor.
Analog soil moisture sensor.
PH-4502C pH sensor.
SH1106 OLED display.
Breadboard, jumper wires, and resistor.

Add the final pin mapping and explain the physical circuit briefly.

Use these images here:
docs/group-evidence/Physical-circuit photo.jpeg - physical circuit setup.
docs/group-evidence/Group2-photo.jpeg - group/lab evidence, if required.

4.4 Firmware setup
Explain that the ESP32 used MicroPython. Mention the main files:
esp32/main.py - main program loop.
esp32/config.py - pins, WiFi, MQTT, Firebase, and calibration settings.
esp32/sensors.py - sensor reading functions.
esp32/oled_display.py - OLED display output.
esp32/mqtt_manager.py - MQTT connection and publishing.
esp32/firebase_client.py - Firebase upload.

Explain the program flow:
Initialize sensors.
Connect to WiFi.
Read temperature, humidity, moisture, and pH.
Show readings on the OLED.
Publish the JSON payload over MQTT.
Upload the reading to Firebase.
Save/prepare readings for dashboard demonstration.

Example payload:
```json
{
  "bed_id": "BED_001",
  "device": "ESP32-IOT-SYSTEM",
  "temperature": 22.9,
  "humidity": 61.4,
  "moisture_percent": 61.67,
  "ph": 14,
  "mqtt_status": "published",
  "firebase_status": "published"
}
```

4.5 Cloud and dashboard setup
Explain:
MQTT was tested using a local Mosquitto broker.
Firebase was used to store readings.
The dashboard reads Firebase-ready JSON data and displays the readings for demonstration.

Mention these files:
data/readings.txt - readable serial-monitor log.
data/firebase-readings.json - cleaned JSON readings.
dashboard/ - dashboard files.

SECTION 5 - TESTING AND RESULTS
This section should show proof that the system worked. Use the screenshots in order and explain each one briefly.

5.1 ESP32 setup and firmware installation
Use:
docs/group-evidence/screenshots/1a.ESP32-detected-on-device-manager.png - ESP32 detected by the laptop.
docs/group-evidence/screenshots/1b.ESP32-communication-error-and-fix.png - COM port communication issue and fix.
docs/group-evidence/screenshots/2a.Erasing-ESP32-flash-memory.png - ESP32 flash erased.
docs/group-evidence/screenshots/2b.Installing-new-firmware.png - MicroPython firmware installed.

Explain that the ESP32 was detected, a port issue was fixed, flash memory was erased, and MicroPython firmware was installed.

5.2 OLED and sensor testing
Use:
docs/group-evidence/screenshots/3a.OLED-test-error.png - OLED/I2C detection problem.
docs/group-evidence/screenshots/3b.OLED-test-fix.png - OLED detected after wiring fix.
docs/group-evidence/screenshots/4a.DHT22-sensor-error.png - DHT22 reading problem.
docs/group-evidence/screenshots/4b.DHT22-sensor-fix.png - DHT22 and sensor readings working.

Explain that some problems were caused by wiring and were fixed during physical testing.

5.3 WiFi and MQTT testing
Use:
docs/group-evidence/screenshots/5a.Wifi-error.png - WiFi connection error.
docs/group-evidence/screenshots/5b.Wifi-error-fix.png - WiFi connected after fixing configuration.
docs/group-evidence/screenshots/6.MQTT-publishing&subscribing.png - MQTT publish and subscribe test.

Explain that WiFi was required before MQTT publishing, and MQTT confirmed that ESP32 readings could be received by the local computer.

5.4 Firebase testing
Use:
docs/group-evidence/screenshots/7a.Firebase-publishing-success.png - Firebase publish success.
docs/group-evidence/screenshots/7b.RealtimeDatabase-readings.jpeg - readings shown in Firebase Realtime Database.
docs/group-evidence/screenshots/7c.FirestoreDatabase-readings.png - stored readings/database evidence, if included in the final setup.

Explain that Firebase confirmed cloud/database storage of readings.

5.5 Final readings and dashboard
Use:
data/readings.txt - sample serial output.
data/firebase-readings.json - 29 cleaned JSON readings.
Dashboard screenshot - add one if available.

Explain that the collected readings were used to demonstrate dashboard visualization.

SECTION 6 - CHALLENGES AND LIMITATIONS
Challenges:
ESP32 port communication.
Firmware flashing.
OLED wiring/I2C detection.
DHT22 sensor wiring.
WiFi configuration.
MQTT setup.
Firebase publishing.
Sensor calibration.

Limitations:
The prototype monitors one setup.
It depends on WiFi.
It is built on a breadboard.
pH and moisture readings need better calibration.
The dashboard currently uses local Firebase-ready JSON data for demonstration.
There is no automated control or SMS/email alerting yet.

SECTION 7 - CONCLUSION AND FUTURE WORK
Conclusion:
Summarize what was completed: sensor readings, OLED display, MQTT publishing, Firebase upload, saved readings, and dashboard visualization.

Realistic future work:
Connect the dashboard directly to live Firebase data.
Add simple threshold alerts on the dashboard.
Improve pH and moisture calibration.
Test more than one ESP32 device.
Use a better enclosure for outdoor/farm use.
Add solar or battery power testing.
Collect more data over a longer period before trying prediction or AI.

REFERENCES
Use 8-12 good references:
ESP32 documentation.
DHT22 datasheet.
PH-4502C/pH sensor documentation.
Soil moisture sensor documentation.
MQTT documentation.
Firebase documentation.
Vermiculture references.
IoT in agriculture references.

APPENDICES
Appendix A - Source code or GitHub link.
Appendix B - Circuit diagram and sensor datasheets.
Appendix C - Sample raw readings.
Appendix D - Group evidence: photos, screenshots, and task contribution log.
