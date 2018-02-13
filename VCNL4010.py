# VCNL4010.py - File for interfacing with the VCNL4010 infrared proximity sensor

# Class: VCNL4010_sensor

# Methods: __init__: Constructor for the class: sets up a VCNL4010 sensor for a given I2C port.
#          read_al: Method for taking an ambient light measurement using the VCNL4010 sensor.
#          interrupt_initial_setup: Method for setting up the interrupt for a new sensor for the proximity measurements.
#          interrupt_reset: Method for resetting the interrupt after its handler has been executed.
#          interrupt_setup_closed_state: Method for setting up the interrupt activate when the proximity sensor senses that an object is further than the treshold.
#          interrupt_setup_open_state: Method for setting up the interrupt activate when the proximity sensor senses that an object is further than the treshold.


class VCNL4010_sensor:

    # Import the necessary modules
    from micropython import const
    from machine import I2C

    # Define device constants
    __SENSOR_ADDR = const(0x13)                 # Address of the device is fixed 0x13

    __COMMAND_REG_ADDR = const(0x80)            # VCNL4010 Command register:                  Register address: 0x80
    __PROX_RATE_REG_ADDR = const(0x82)          # VCNL4010 Proximity rate register:           Register address: 0x82
    __IR_LED_CURRENT_REG_ADDR = const(0x83)     # VCNL4010 IR LED current register:           Register address: 0x83
    __ALS_RESULT_REG_ADDR = const(0x85)         # VCNL4010 Ambient light result register #5:  Register address: 0x85 / High byte of the 16 bit result
    __INT_CONTROL_REG_ADDR = const(0x89)        # VCNL4010 Interrupt control Register:        Register address: 0x89
    __LOW_THRE_REG_ADDR_HIGH = const(0x8A)      # VCNL4010 Low threshold register high byte:  Register address: 0x8A
    __LOW_THRE_REG_ADDR_LOW = const(0x8B)       # VCNL4010 Low threshold register low byte:   Register address: 0x8B
    __HIGH_THRE_REG_ADDR_HIGH = const(0x8C)     # VCNL4010 High threshold register high byte: Register address: 0x8C
    __HIGH_THRE_REG_ADDR_LOW = const(0x8D)      # VCNL4010 High threshold register low byte:  Register address: 0x8D
    __INT_STATUS_REG_ADDR = const(0x8E)         # VCNL4010 Interrupt status register:         Register address: 0x8E

    # Define other constants
    DATA_NOT_READY = const(-1)

    # The VCNL4010 poximity readings correspond to how close the object is from the sensor. This means the closer the object is to the device,
    # the larger the result that the sensor returs. 
    PROX_THRESHOLD_HIGH = const(0x09)   # Threshold to decide whether the postbox flap is close (closed) or far (open) from the sensor - high byte
    PROX_THRESHOLD_LOW = const(0x06)    #                                                                                              - low byte

    # Methods:

    # __init__: This is the constructor of the class, it creates an instance of the sensor with the specified I2C port.
    def __init__(self, i2cport):

        self.i2cport = i2cport

    # read_al: This method returns a single ambient light measurement with the VCNL4010 sensor.
    def read_al(self):

        # First checking if there is data available from the sensor to read.
        self.i2cport.writeto(__SENSOR_ADDR, bytearray([__COMMAND_REG_ADDR]))
        command_reg_data = self.i2cport.readfrom(__SENSOR_ADDR, 1)
        dataReady = int.from_bytes(command_reg_data, 'big') & (1 << 6)

        # If there is no data ready...
        if dataReady == 0:

            # ...we set the sensor to do an on-demand ambient light measurement...
            if (int.from_bytes(command_reg_data, 'big') & (1 << 4)) == 0:
                self.i2cport.writeto(__SENSOR_ADDR, bytearray([__COMMAND_REG_ADDR, 0x10]))
            return DATA_NOT_READY # ... and return that there is no data ready.

        # Else we read the data from the sensor and return it.    
        self.i2cport.writeto(__SENSOR_ADDR, bytearray([__ALS_RESULT_REG_ADDR]))
        data = self.i2cport.readfrom(__SENSOR_ADDR, 2)
        return int.from_bytes(data, 'big')


    # interrupt_initial_setup: Initialise the interrupt to activate when the proximity reading is below the threshold (postbox flap is closed).
    def interrupt_initial_setup(self):

        self.i2cport.writeto(__SENSOR_ADDR, bytearray([__LOW_THRE_REG_ADDR_LOW, PROX_THRESHOLD_LOW]))    # set low threshold to PROX_THRESHOLD
        self.i2cport.writeto(__SENSOR_ADDR, bytearray([__LOW_THRE_REG_ADDR_HIGH, PROX_THRESHOLD_HIGH]))
        self.i2cport.writeto(__SENSOR_ADDR, bytearray([__HIGH_THRE_REG_ADDR_LOW, 0xFF]))                 # set high threshold to maximum
        self.i2cport.writeto(__SENSOR_ADDR, bytearray([__HIGH_THRE_REG_ADDR_HIGH, 0xFF]))
        self.i2cport.writeto(__SENSOR_ADDR, bytearray([__IR_LED_CURRENT_REG_ADDR, 0xFF]))                # set the IR LED current value to maximum (200mA) - device sensitivity is 20cm (max)
        self.i2cport.writeto(__SENSOR_ADDR, bytearray([__COMMAND_REG_ADDR, 0x00]))                       # set command register to 0, so that we can set the proximity reading rate
        self.i2cport.writeto(__SENSOR_ADDR, bytearray([__PROX_RATE_REG_ADDR, 0x02]))                     # set the proximity reading rate to 1.95 readings per sec
        self.i2cport.writeto(__SENSOR_ADDR, bytearray([__COMMAND_REG_ADDR, 0x03]))                       # set sensor to measure proximity with self-timed measurements
        self.i2cport.writeto(__SENSOR_ADDR, bytearray([__INT_CONTROL_REG_ADDR, 0x52]))                   # set interrupt control register to threshold exceed mode

    # interrupt_reset: Clears the interrupt status bits by writing a '1' to the low threshold and the high threshold exceed status indicator bit.
    def interrupt_reset(self):
        self.i2cport.writeto(__SENSOR_ADDR, bytearray([__INT_STATUS_REG_ADDR, 0x03])) # clear interrupt status bits

    # interrupt_setup_closed_state: This method sets up the interrupt to activate when the proximity reading is below the threshold. (no objects close to the sensor)
    #                               With this setup we detect when the postbox flap has been opened.
    def interrupt_setup_closed_state(self):

        self.i2cport.writeto(__SENSOR_ADDR, bytearray([__LOW_THRE_REG_ADDR_LOW, PROX_THRESHOLD_LOW]))      # set low threshold to PROX_THRESHOLD
        self.i2cport.writeto(__SENSOR_ADDR, bytearray([__LOW_THRE_REG_ADDR_HIGH, PROX_THRESHOLD_HIGH]))
        self.i2cport.writeto(__SENSOR_ADDR, bytearray([__HIGH_THRE_REG_ADDR_LOW, 0xFF]))                   # set high threshold to maximum
        self.i2cport.writeto(__SENSOR_ADDR, bytearray([__HIGH_THRE_REG_ADDR_HIGH, 0xFF]))
        self.i2cport.writeto(__SENSOR_ADDR, bytearray([__INT_CONTROL_REG_ADDR, 0x52]))                     # reset interrupt control register for threshold exceed mode

    # interrupt_setup_open_state: This method sets up the interrupt to activate when the proximity reading is above the threshold (an object is close to the sensor).
    #                             With this setup we detect when the postbox flap has closed.
    def interrupt_setup_open_state(self):

        self.i2cport.writeto(__SENSOR_ADDR, bytearray([__LOW_THRE_REG_ADDR_LOW, 0x00]))                    # set low threshold to minimum
        self.i2cport.writeto(__SENSOR_ADDR, bytearray([__LOW_THRE_REG_ADDR_HIGH, 0x00]))
        self.i2cport.writeto(__SENSOR_ADDR, bytearray([__HIGH_THRE_REG_ADDR_LOW, PROX_THRESHOLD_LOW]))     # set high threshold to PROX_THRESHOLD
        self.i2cport.writeto(__SENSOR_ADDR, bytearray([__HIGH_THRE_REG_ADDR_HIGH, PROX_THRESHOLD_HIGH]))
        self.i2cport.writeto(__SENSOR_ADDR, bytearray([__INT_CONTROL_REG_ADDR, 0x52]))                     # reset interrupt control register for threshold exceed mode
