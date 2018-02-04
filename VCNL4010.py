# VCNL4010.py - File for interfacing with the VCNL4010 Infrared proximity sensor

class Sensor:

    from micropython import const
    from machine import I2C

    __SENSOR_ADDR = const(0x13)
    __COMMAND_REG_ADDR = const(0x80)
    __PROX_RESULT_REG_ADDR = const(0x87)
    __ALS_RESULT_REG_ADDR = const(0x85)

    DATA_NOT_READY = const(-1)

    def __init__(self, i2cport, selftimed=False, prox_en=False, als_en=False,
                    prox_od=False, als_od=False):
        self.i2cport = i2cport
        self.config = 0x0 | selftimed | prox_od << 3 | als_od << 4
        instructionBuffer = bytearray([__COMMAND_REG_ADDR, self.config])
        i2cport.writeto(__SENSOR_ADDR, instructionBuffer)
        if prox_en | als_en :
            self.config = self.config | prox_en << 1 | prox_en << 2
            instructionBuffer[1] = self.config
            i2cport.writeto(__SENSOR_ADDR, instructionBuffer);

    def read_prox(self):
        self.i2cport.writeto(__SENSOR_ADDR, bytearray([__COMMAND_REG_ADDR]))
        command_reg_data = self.i2cport.readfrom(__SENSOR_ADDR, 1)
        dataReady = int.from_bytes(command_reg_data, 'big') & (1 << 5)
        if dataReady == 0:
            return DATA_NOT_READY
        self.i2cport.writeto(__SENSOR_ADDR, bytearray([__PROX_RESULT_REG_ADDR]))
        data = self.i2cport.readfrom(__SENSOR_ADDR, 2)
        return int.from_bytes(data, 'big')

    def read_als(self):
        self.i2cport.writeto(__SENSOR_ADDR, bytearray([__COMMAND_REG__ADDR]))
        command_reg_data = self.i2cport.readfrom(__SENSOR_ADDR, 1)
        dataReady = int.from_bytes(command_reg_data, 'big') & (1 << 6)
        if dataReady == 0:
            return DATA_NOT_READY
        self.i2cport.writeto(__SENSOR_ADDR, bytearray([__ALS_RESULT_REG_ADDR]))
        data = self.i2cport.readfrom(__SENSOR_ADDR, 2)
        return int.from_bytes(data, 'big')

