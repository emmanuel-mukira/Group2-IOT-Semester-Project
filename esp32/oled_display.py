from machine import Pin, I2C

from config import OLED_SDA, OLED_SCL
from sh1106 import SH1106_I2C


oled = None


def init_oled():
    """
    Initializes the SH1106 OLED display and prints the I2C scan result.
    """

    global oled

    i2c = I2C(
        0,
        scl=Pin(OLED_SCL),
        sda=Pin(OLED_SDA),
        freq=100000
    )

    print("I2C scan:", i2c.scan())

    oled = SH1106_I2C(128, 64, i2c, addr=0x3C)
    oled_message("IoT System", "OLED Ready", "Starting...")

    return oled


def oled_message(line1="", line2="", line3="", line4="", line5="", line6=""):
    """
    Displays up to six short text lines on the OLED.
    """

    if oled is None:
        return

    oled.fill(0)
    oled.text(line1, 0, 0)
    oled.text(line2, 0, 10)
    oled.text(line3, 0, 20)
    oled.text(line4, 0, 30)
    oled.text(line5, 0, 40)
    oled.text(line6, 0, 50)
    oled.show()


def show_value(value, decimals=1):
    """
    Formats sensor values for the OLED.
    """

    if value is None:
        return "N/A"

    return str(round(value, decimals))


def display_sensor_data(dht_temp, dht_hum, moisture_percent, ph, ph_voltage):
    """
    Displays readings on the OLED.

    Shows:
    - Selected DHT sensor temperature
    - Selected DHT sensor humidity
    - Soil moisture percentage
    - pH value
    - pH voltage
    """

    if oled is None:
        return

    oled.fill(0)

    oled.text("IoT Sensor Data", 0, 0)
    oled.text("Air:" + show_value(dht_temp) + "C", 0, 10)
    oled.text("Hum:" + show_value(dht_hum, 0) + "%", 0, 20)
    oled.text("Moist:" + str(round(moisture_percent, 1)) + "%", 0, 30)
    oled.text("pH:" + str(round(ph, 2)), 0, 40)
    oled.text("pH V:" + str(round(ph_voltage, 2)), 0, 50)

    oled.show()


def display_error(error):
    """
    Shows a compact error message while keeping the main loop alive.
    """

    oled_message("System Error", str(error)[:16], "Still running...")
