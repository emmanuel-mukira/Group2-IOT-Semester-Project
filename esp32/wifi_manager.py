# =================================================
# wifi_manager.py
# WiFi connection logic
# =================================================

import network
import time

from config import WIFI_SSID, WIFI_PASSWORD
from oled_display import oled_message


def connect_wifi():
    """
    Connects ESP32 to WiFi.

    CHANGE:
    Update WIFI_SSID and WIFI_PASSWORD in config.py.
    """

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
        ip_address = wlan.ifconfig()[0]

        print("WiFi connected")
        print("IP:", ip_address)

        oled_message("WiFi Connected", ip_address)
        time.sleep(1)

        return True

    else:
        print("WiFi failed")
        oled_message("WiFi Failed", "Check hotspot")

        return False