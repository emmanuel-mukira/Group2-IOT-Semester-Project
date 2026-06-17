from machine import Pin, ADC
import time
import dht

from config import (
    DHT_PIN,
    DHT_SENSOR_TYPE,
    MOISTURE_PIN,
    PH_PIN,
    DHT_TEMP_OFFSET,
    DHT_HUM_OFFSET,
    ADC_MAX_VALUE,
    ADC_REFERENCE_VOLTAGE,
    MOISTURE_DRY_RAW,
    MOISTURE_WET_RAW,
    PH_NEUTRAL_VOLTAGE,
    PH_SLOPE
)


dht_sensor = None
moisture_adc = None
ph_adc = None


def init_sensors():
    """
    Initializes the DHT22, soil moisture sensor, and pH sensor.
    """

    global dht_sensor, moisture_adc, ph_adc

    dht_sensor = dht.DHT22(Pin(DHT_PIN, Pin.IN, Pin.PULL_UP))
    print("DHT22 initialized on GPIO", DHT_PIN)

    moisture_adc = ADC(Pin(MOISTURE_PIN))
    moisture_adc.atten(ADC.ATTN_11DB)
    print("Soil moisture sensor initialized on GPIO", MOISTURE_PIN)

    ph_adc = ADC(Pin(PH_PIN))
    ph_adc.atten(ADC.ATTN_11DB)
    print("PH-4502C sensor initialized on GPIO", PH_PIN)


def read_dht():
    """
    Reads temperature and humidity from the selected DHT sensor.
    """

    try:
        # DHT sensors need a delay between readings.
        time.sleep(2)

        dht_sensor.measure()

        temp = dht_sensor.temperature()
        hum = dht_sensor.humidity()

        temp = temp + DHT_TEMP_OFFSET
        hum = hum + DHT_HUM_OFFSET

        return temp, hum

    except Exception as e:
        print("DHT read error:", e)
        return None, None


def read_adc_average(adc, samples=10):
    """
    Takes several ADC readings and returns the average.
    This reduces noise from analog sensors.
    """

    total = 0

    for i in range(samples):
        total += adc.read()
        time.sleep_ms(30)

    return total // samples


def read_moisture():
    raw = read_adc_average(moisture_adc)

    moisture_percent = (
        (MOISTURE_DRY_RAW - raw) /
        (MOISTURE_DRY_RAW - MOISTURE_WET_RAW)
    ) * 100

    if moisture_percent < 0:
        moisture_percent = 0

    if moisture_percent > 100:
        moisture_percent = 100

    return raw, moisture_percent


def read_ph():
    raw = read_adc_average(ph_adc)

    voltage = (raw / ADC_MAX_VALUE) * ADC_REFERENCE_VOLTAGE

    ph = 7 + ((voltage - PH_NEUTRAL_VOLTAGE) * PH_SLOPE)

    if ph < 0:
        ph = 0

    if ph > 14:
        ph = 14

    return raw, voltage, ph

