from machine import Pin, SoftI2C
from sh1106 import SH1106_I2C
import time

WIDTH = 128
HEIGHT = 64

SCL_PIN = 18
SDA_PIN = 19

print("Starting SH1106 OLED test...")

i2c = SoftI2C(
    scl=Pin(SCL_PIN, Pin.OPEN_DRAIN, Pin.PULL_UP),
    sda=Pin(SDA_PIN, Pin.OPEN_DRAIN, Pin.PULL_UP),
    freq=100000
)

devices = i2c.scan()

print("I2C scan result:")
print([hex(device) for device in devices])

if 0x3C in devices:
    oled_addr = 0x3C
elif 0x3D in devices:
    oled_addr = 0x3D
else:
    print("OLED not detected at 0x3C or 0x3D.")
    print("Check VCC, GND, SCK/SCL, SDA, and try 5V if module supports it.")
    raise SystemExit

oled = SH1106_I2C(WIDTH, HEIGHT, i2c, addr=oled_addr)

oled.fill(0)
oled.text("Group 2 IoT", 0, 0)
oled.text("SH1106 OLED", 0, 16)
oled.text("ESP32 Ready", 0, 32)
oled.text("Addr: " + hex(oled_addr), 0, 48)
oled.show()

print("OLED test complete using address:", hex(oled_addr))

while True:
    time.sleep(1)