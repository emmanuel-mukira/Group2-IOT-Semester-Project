# =================================================
# wifi_manager.py
# WiFi connection logic
# =================================================

import network
import time

from config import WIFI_SSID, WIFI_PASSWORD
from oled_display import oled_message


def reset_wifi(wlan):
    """
    Resets the ESP32 station interface before a fresh connection attempt.
    """

    try:
        if wlan.isconnected():
            wlan.disconnect()
            time.sleep(1)
    except Exception as e:
        print("WiFi disconnect warning:", e)

    try:
        wlan.active(False)
        time.sleep(2)
        wlan.active(True)
        time.sleep(2)
    except Exception as e:
        print("WiFi reset warning:", e)


def connect_wifi():
    """
    Connects ESP32 to WiFi.

    CHANGE:
    Update WIFI_SSID and WIFI_PASSWORD in config.py.
    """

    try:
        ap = network.WLAN(network.AP_IF)
        ap.active(False)
    except Exception as e:
        print("WiFi AP disable warning:", e)

    wlan = network.WLAN(network.STA_IF)
    reset_wifi(wlan)

    if not wlan.isconnected():
        print("Connecting to WiFi...")
        oled_message("Connecting", "to WiFi...")

        try:
            wlan.connect(WIFI_SSID, WIFI_PASSWORD)
        except OSError as e:
            print("WiFi connect start failed:", e)
            oled_message("WiFi Failed", "State error")
            return False

        timeout = 30

        while not wlan.isconnected() and timeout > 0:
            try:
                print("WiFi status:", wlan.status())
            except Exception:
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

