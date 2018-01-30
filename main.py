# main.py - this file excutes automatically after boot.py

# Import the necessary modules
from micropython import const
from machine import Pin, I2C

SCL_PIN = const(5)
SDA_PIN = const(4)
SDA_FREQ = const(3400 * 1000)
PROX_SENSOR_ADDRESS = const(0x13)
COMMAND_REG_ADDRESS = const(0x80)

# Create the I2C port
i2cport = I2C(scl=Pin(SCL_PIN), sda=Pin(SDA_PIN), freq=SDA_FREQ)

#IR sensor config
instructionBuffer = bytearray([COMMAND_REG_ADDRESS, 0xE4])
i2cport.writeto(PROX_SENSOR_ADDRESS, instructionBuffer)

#Poll for proximity data
proxReady = 1
while proxReady != 0 :
    i2cport.writeto(PROX_SENSOR_ADDRESS, bytearray([COMMAND_REG_ADDRESS]))
    command_reg_data = i2cport.readfrom(PROX_SENSOR_ADDRESS, 1)
    print(command_reg_data);
    proxRead = int.from_bytes(command_reg_data, 'big') & (1 << 5)
    print("Polled")

>>>>>>> 1dba9a5... main.py: Set up communication to board and sensor
