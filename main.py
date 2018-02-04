# main.py - this file excutes automatically after boot.py

# Import the necessary modules
from micropython import const
from machine import Pin, I2C
from VCNL4010 import Sensor
import time

SCL_PIN = const(5)
SDA_PIN = const(4)
SDA_FREQ = const(3400 * 1000)

# Create the I2C port
i2cport = I2C(scl=Pin(SCL_PIN), sda=Pin(SDA_PIN), freq=SDA_FREQ)

#IR sensor config
prox_and_als_sensor = Sensor(i2cport, selftimed=True, prox_en=True)

#Poll for proximity data
while True:
    proxData = Sensor.DATA_NOT_READY
    while proxData == Sensor.DATA_NOT_READY :
        proxData = prox_and_als_sensor.read_prox()

    print(proxData)
    time.sleep_ms(20)
