from machine import Pin, SoftI2C
import time

print("Testing OLED on default ESP32 I2C pins")

i2c = SoftI2C(
    scl=Pin(22, Pin.OPEN_DRAIN, Pin.PULL_UP),
    sda=Pin(21, Pin.OPEN_DRAIN, Pin.PULL_UP),
    freq=100000
)

time.sleep(1)

devices = i2c.scan()

print("Devices found:")
print([hex(device) for device in devices])