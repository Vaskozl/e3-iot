# main.py - this file excutes automatically after boot.py


# Import network and mqtt
from net import *

# Import the necessary modules
from micropython import const
from machine import Pin, I2C
import time

SCL_PIN = const(5)
SDA_PIN = const(4)
SDA_FREQ = const(3400 * 1000)
PROX_SENSOR_ADDRESS = const(0x13)
COMMAND_REG_ADDRESS = const(0x80)
PROX_RESULT_REG_ADDRESS = const(0x87)

BROKER_ADDRESS = '192.168.0.10'
TOPIC_PREFIX = 'esys/just_another_group/'

# Create the I2C port
i2cport = I2C(scl=Pin(SCL_PIN), sda=Pin(SDA_PIN), freq=SDA_FREQ)

#IR sensor config
instructionBuffer = bytearray([COMMAND_REG_ADDRESS, 0x81])
i2cport.writeto(PROX_SENSOR_ADDRESS, instructionBuffer)
instructionBuffer[1] = 0x83
i2cport.writeto(PROX_SENSOR_ADDRESS, instructionBuffer)

# Connect to wifi
wpa_init()

# Init mqtt
mqtt = Mqtt(BROKER_ADDRESS, TOPIC_PREFIX)
mqtt.connect()

#Poll for proximity data
while True:
    proxReady = 0
    while proxReady == 0 :
        i2cport.writeto(PROX_SENSOR_ADDRESS, bytearray([COMMAND_REG_ADDRESS]))
        command_reg_data = i2cport.readfrom(PROX_SENSOR_ADDRESS, 1)
        proxReady = int.from_bytes(command_reg_data, 'big') & (1 << 5)

    proxData = bytearray(2)
    i2cport.writeto(PROX_SENSOR_ADDRESS, bytearray([PROX_RESULT_REG_ADDRESS]))
    proxData = i2cport.readfrom(PROX_SENSOR_ADDRESS, 2)
    print(proxData)
    mqtt.send('proximity', proxData)
    time.sleep_ms(200)
