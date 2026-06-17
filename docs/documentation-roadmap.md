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

SECTION 3 - BACKGROUND / LITERATURE REVIEW
Keep this section simple. Cover only:
Basic vermiculture conditions: temperature, moisture, humidity, and pH.
How IoT helps in agriculture.
Why MQTT is useful for sending small sensor readings.
Why Firebase is suitable for storing simple JSON readings in this prototype.

Do not include a long comparison of MongoDB, PostgreSQL, LoRa, AI, or other systems unless the lecturer specifically asks for it.

SECTION 4 - SYSTEM DESIGN
Include:
A simple system diagram showing:
Sensors -> ESP32 -> OLED display -> MQTT/Firebase -> Dashboard.

Hardware used:
ESP32 development board.
DHT22 temperature and humidity sensor.
Analog soil moisture sensor.
PH-4502C pH sensor.
SH1106 OLED display.
Breadboard, jumper wires, and resistor.

Also include:
Final pin mapping.
Circuit diagram or clear circuit photo.
Example JSON payload sent by the ESP32.

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

SECTION 5 - IMPLEMENTATION
Explain what you built in a practical way:
How the sensors were connected to the ESP32.
How the ESP32 reads sensor values.
How readings are shown on the OLED.
How WiFi connection works.
How MQTT publishing works.
How Firebase upload works.
How the dashboard displays the saved readings.

Mention the main project files:
esp32/main.py
esp32/config.py
esp32/sensors.py
esp32/oled_display.py
esp32/mqtt_manager.py
esp32/firebase_client.py
dashboard/
data/readings.txt
data/firebase-readings.json

Use only short code snippets where they help explain the work.

SECTION 6 - TESTING AND RESULTS
Show proof that the system worked.

Include:
ESP32 detected and firmware installed.
OLED test result.
DHT22 test result.
WiFi connection result.
MQTT publish result.
Firebase publish result.
Dashboard screenshot.
Sample readings from the 29 cleaned readings.

Mention any issues fixed during testing, for example OLED setup, DHT22 setup, WiFi errors, or Firebase publishing.

SECTION 7 - CHALLENGES AND LIMITATIONS
Challenges:
Wiring and sensor setup.
ESP32 firmware flashing.
WiFi connection.
MQTT testing.
Firebase upload.
Sensor calibration.

Limitations:
The prototype monitors one setup.
It depends on WiFi.
It is built on a breadboard.
pH and moisture readings need better calibration.
The dashboard currently uses local Firebase-ready JSON data for demonstration.
There is no automated control or SMS/email alerting yet.

SECTION 8 - CONCLUSION AND FUTURE WORK
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
