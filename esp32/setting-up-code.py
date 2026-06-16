from machine import Pin, ADC, I2C, unique_id
import time
import network
import ujson
import framebuf
import dht
import urequests  # <-- Added for Firebase
from ubinascii import hexlify

try:
    from umqtt.simple import MQTTClient
except:
    MQTTClient = None

# =================================================
# CLOUD SETTINGS
# =================================================
USE_MQTT = True
USE_FIREBASE = True  # <-- Set to True to enable Firebase upload

WIFI_SSID = "K8597"
WIFI_PASSWORD = "00001111"

MQTT_BROKER = "192.168.137.89" 
MQTT_PORT = 1883
MQTT_TOPIC = "iot/lab/sensor"
MQTT_CLIENT_ID = b"esp32-soil-ph-dht22-" + hexlify(unique_id())

# PASTE YOUR FIREBASE URL HERE (Make sure it ends with /latest_readings.json)
FIREBASE_URL = "https://iot-vermiq-default-rtdb.firebaseio.com/latest_readings.json"

# =================================================
# PIN SETTINGS
# =================================================
OLED_SDA = 21
OLED_SCL = 22

DHT22_PIN = 4

MOISTURE_PIN = 34
PH_PIN = 35

# =================================================
# CALIBRATION
# =================================================
DHT_TEMP_OFFSET = 0.0   
DHT_HUM_OFFSET = 0.0

# =================================================
# SH1106 OLED DRIVER
# =================================================
class SH1106_I2C(framebuf.FrameBuffer):
    def __init__(self, width, height, i2c, addr=0x3C):
        self.width = width
        self.height = height
        self.i2c = i2c
        self.addr = addr
        self.pages = self.height // 8
        self.buffer = bytearray(self.width * self.pages)
        super().__init__(self.buffer, self.width, self.height, framebuf.MONO_VLSB)
        self.init_display()

    def write_cmd(self, cmd):
        self.i2c.writeto(self.addr, bytearray([0x00, cmd]))

    def write_data(self, data):
        self.i2c.writeto(self.addr, bytearray([0x40]) + data)

    def init_display(self):
        cmds = [
            0xAE, 0xD5, 0x80, 0xA8, 0x3F,
            0xD3, 0x00, 0x40, 0xAD, 0x8B,
            0xA1, 0xC8, 0xDA, 0x12, 0x81,
            0xCF, 0xD9, 0xF1, 0xDB, 0x40,
            0xA4, 0xA6, 0xAF
        ]

        for cmd in cmds:
            self.write_cmd(cmd)

        self.fill(0)
        self.show()

    def show(self):
        column_offset = 2

        for page in range(self.pages):
            self.write_cmd(0xB0 + page)
            self.write_cmd(0x00 + (column_offset & 0x0F))
            self.write_cmd(0x10 + ((column_offset >> 4) & 0x0F))

            start = self.width * page
            end = start + self.width
            self.write_data(self.buffer[start:end])

# =================================================
# OLED SETUP
# =================================================
i2c = I2C(0, scl=Pin(OLED_SCL), sda=Pin(OLED_SDA), freq=100000)

print("I2C scan:", i2c.scan())

oled = SH1106_I2C(128, 64, i2c, addr=0x3C)

def oled_message(line1="", line2="", line3="", line4="", line5="", line6=""):
    oled.fill(0)
    oled.text(line1, 0, 0)
    oled.text(line2, 0, 10)
    oled.text(line3, 0, 20)
    oled.text(line4, 0, 30)
    oled.text(line5, 0, 40)
    oled.text(line6, 0, 50)
    oled.show()

oled_message("IoT System", "OLED Ready", "Starting...")

# =================================================
# SENSOR SETUP
# =================================================
dht22_sensor = dht.DHT22(Pin(DHT22_PIN, Pin.IN, Pin.PULL_UP))

moisture_adc = ADC(Pin(MOISTURE_PIN))
moisture_adc.atten(ADC.ATTN_11DB)

ph_adc = ADC(Pin(PH_PIN))
ph_adc.atten(ADC.ATTN_11DB)

# =================================================
# WIFI + MQTT FUNCTIONS
# =================================================
def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)

    if not wlan.isconnected():
        print("Connecting to WiFi...")
        oled_message("Connecting", "to WiFi...")
        wlan.connect(WIFI_SSID, WIFI_PASSWORD)

        timeout = 30
        while not wlan.isconnected() and timeout > 0:
            print(".", end="")
            time.sleep(1)
            timeout -= 1

    print()

    if wlan.isconnected():
        print("WiFi connected")
        print("IP:", wlan.ifconfig()[0])
        oled_message("WiFi Connected", wlan.ifconfig()[0])
        time.sleep(1)
        return True
    else:
        print("WiFi failed")
        oled_message("WiFi Failed", "Check hotspot")
        return False

def connect_mqtt():
    if MQTTClient is None:
        print("MQTT library not available")
        return None

    client = MQTTClient(
        client_id=MQTT_CLIENT_ID,
        server=MQTT_BROKER,
        port=MQTT_PORT,
        keepalive=60
    )

    client.connect()
    print("MQTT connected")
    oled_message("MQTT Connected", "Ready")
    time.sleep(1)
    return client

# =================================================
# SENSOR READ FUNCTIONS
# =================================================
def read_dht22():
    try:
        time.sleep(2)
        dht22_sensor.measure()

        temp = dht22_sensor.temperature()
        hum = dht22_sensor.humidity()

        temp = temp + DHT_TEMP_OFFSET
        hum = hum + DHT_HUM_OFFSET

        return temp, hum

    except Exception as e:
        print("DHT22 read error:", e)
        return None, None


def read_adc_average(adc, samples=10):
    total = 0
    for i in range(samples):
        total += adc.read()
        time.sleep_ms(30)
    return total // samples


def read_moisture():
    raw = read_adc_average(moisture_adc)
    moisture_percent = (raw / 4095) * 100
    return raw, moisture_percent


def read_ph():
    raw = read_adc_average(ph_adc)
    voltage = (raw / 4095) * 3.3
    ph = 7 + ((2.5 - voltage) / 0.18)
    return raw, voltage, ph


def show_value(value, decimals=1):
    if value is None:
        return "N/A"
    return str(round(value, decimals))

# =================================================
# MAIN PROGRAM
# =================================================
client = None

if USE_MQTT or USE_FIREBASE:
    if connect_wifi():
        if USE_MQTT:
            client = connect_mqtt()
    else:
        USE_MQTT = False
        USE_FIREBASE = False

print("Starting final IoT system...")
print("OLED enabled")
print("DHT22 on GPIO4")
print("Moisture on GPIO34")
print("pH on GPIO35")
print("--------------------------------------")

oled_message("System Ready", "DHT22 GPIO4", "Moisture + pH")
time.sleep(2)

while True:
    try:
        dht22_temp, dht22_hum = read_dht22()
        moisture_raw, moisture_percent = read_moisture()
        ph_raw, ph_voltage, ph = read_ph()

        print("DHT22 Temp:", dht22_temp)
        print("DHT22 Hum:", dht22_hum)
        print("Moisture Raw:", moisture_raw)
        print("Moisture %:", round(moisture_percent, 2))
        print("pH Raw:", ph_raw)
        print("pH Voltage:", round(ph_voltage, 3), "V")
        print("pH:", round(ph, 2))
        print("--------------------------------------")

        oled.fill(0)
        oled.text("IoT Sensor Data", 0, 0)
        oled.text("Air:" + show_value(dht22_temp) + "C", 0, 10)
        oled.text("Hum:" + show_value(dht22_hum, 0) + "%", 0, 20)
        oled.text("Moist:" + str(round(moisture_percent, 1)) + "%", 0, 30)
        oled.text("pH:" + str(round(ph, 2)), 0, 40)
        oled.text("pH V:" + str(round(ph_voltage, 2)), 0, 50)
        oled.show()

        # Build the payload once for both MQTT and Firebase
        payload = {
            "dht22_temp": dht22_temp,
            "dht22_humidity": dht22_hum,
            "moisture_raw": moisture_raw,
            "moisture_percent": round(moisture_percent, 2),
            "ph_raw": ph_raw,
            "ph_voltage": round(ph_voltage, 3),
            "ph": round(ph, 2)
        }

        # 1. Publish to MQTT Local Server
        if USE_MQTT and client is not None:
            try:
                client.publish(MQTT_TOPIC, ujson.dumps(payload))
                print("MQTT published")
            except Exception as e:
                print("MQTT publish failed:", e)

        # 2. Upload to Firebase Realtime Database
        if USE_FIREBASE:
            try:
                # Using PUT overwrites the 'latest_readings' node with the newest data.
                # (If you want a continuous history log instead, change .put to .post)
                res = urequests.put(FIREBASE_URL, data=ujson.dumps(payload))
                print("Firebase published:", res.status_code)
                res.close()  # CRITICAL: Always close the connection to prevent memory errors
            except Exception as e:
                print("Firebase publish failed:", e)

    except Exception as e:
        print("Main loop error:", e)
        oled_message("System Error", str(e)[:16], "Still running...")

    time.sleep(3)

