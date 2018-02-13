# main.py - this file excutes automatically after boot.py

# Glossary: als = Ambient Light Sensor, prox = Proximity Sensor

# Import the necessary modules
from micropython import const
from machine import Pin, I2C, disable_irq, enable_irq, PWM
from VCNL4010 import VCNL4010_sensor
import time

# Define Pin Layout
BUT_IN = const(0)               # D3: Button Pin
MOTOR_CONTROL_PIN = const(2)    # D4: Motor Control Pin
SDA_PIN_prox = const(4)         # D2: I2C Data Pin for the VCNL4010 used as Proximity Sensor
SCL_PIN_prox = const(5)         # D1: I2C Clock Pin for the VCNL4010 used as Proximity Sensor
SDA_PIN_als = const(12)         # D6: I2C Data Pin for the VCNL4010 used as Ambient Light Sensor
SCL_PIN_als = const(13)         # D7: I2C Clock Pin for the VCNL4010 used as Ambient Light Sensor
INT_PROX = const(14)            # D5: Interrupt Pin for Proximity Sensor
LED_PIN = const(16)             # D0: LED Pin

# Define Device constants
SDA_FREQ = const(3400 * 1000) # VCNL4010 I2C clock rate range: 3400 kHz

# Define Motor position constants
DOOR_CLOSED = const(30) # PWM Duty Cycle for servomotor corresponding to a closed door
DOOR_OPEN = const (118) # PWM Duty Cycle for servomotor corresponding to an open door

# Define State Variables
flap_position = 0             # flap_position = 0 when flap is closed, flap_position = 1 when flap is open
change_in_flap_position = 0   # change_in_flap_position = 1 when flap position changed, change_in_flap_position = 0 after program handled the change
closed_flap_counter = 0       # count is incremented when the device detects the flap to be closed
button_pressed = 0            # button_pressed = 1 when button was pressed, button_pressed = 0 after the program handled the press 
door_position = 0             # door position: closed = 0, open = 1

# Create the I2C ports
i2cport_prox = I2C(scl=Pin(SCL_PIN_prox), sda=Pin(SDA_PIN_prox), freq=SDA_FREQ)
i2cport_als = I2C(scl=Pin(SCL_PIN_als), sda=Pin(SDA_PIN_als), freq=SDA_FREQ)

# Create instances of the VCNL4010 class for the sensors
prox_sensor = VCNL4010_sensor(i2cport_prox) # VCNL4010 instance for proximity sensor
als_sensor = VCNL4010_sensor(i2cport_als)   # VCNL4010 instance for als sensor

# Set up interrupt pins on NodeMCU-board
prox_int_pin = Pin(INT_PROX, Pin.IN, Pin.PULL_UP) # pin used for detecting interrupt from prox sensor
button_int_pin = Pin(BUT_IN, Pin.IN, Pin.PULL_UP) # pin used for detecting a button press

# Set up LED pin
led = Pin(LED_PIN, Pin.OUT)
led.value(False) # turn LED initially off

# Set up the pin controlling the servomotor position
# Servomotor position can be changed by altering the duty cycle of a PWM signal (Duty cycle: all off = 0, all on = 1023)
# Servomotor can turn 180 degrees (PWM-duty-cycle-range: 30 - 122)
motor_position = DOOR_CLOSED # starting door position (closed)
servo = PWM(Pin(MOTOR_CONTROL_PIN), freq=50, duty= motor_position) # set up PWM signal for controlling servo position

# Configure proximity sensor to raise an interrupt when flap position changes
prox_sensor.interrupt_initial_setup()    # initial set-up: closed-state waiting for flap to be opened


# Define interrupt handlers
# Interrupt handler responsible for servicing the proximity sensor
def proximity_interrupt_handler(pin):
    global flap_position
    global change_in_flap_position
    global closed_flap_counter #why use global variable

    # if the flap is closed, a single interrupt indicates that flap was opened
    if flap_position == 0:
        change_in_flap_position = 1 # indicates that flap is in new position

    # if flap was opened, 11 interrupts that flap is closed need to be counted (equivalent to x sec.)
    # avoids that several messages are sent out if letters are thrown in individually
    if flap_position == 1:
        closed_flap_counter += 1
        print("number of closed flap detected: " + str(closed_flap_counter))

        if closed_flap_counter > 10: # program recognises the flap to be closed
            change_in_flap_position = 1 # indicates that flap is in new position

        else:
            prox_sensor.interrupt_reset() # VCNL4010 requires to reset the interrupt status register after each interrupt

# Interrupt handler used for servicing the button
def button_interrupt_handler(pin):
    global button_pressed
    print("Button was pressed")
    button_pressed = 1 # indicates that the button was pressed


# Configure interrupt pins to call interrupt handler on falling edge
prox_int_pin.irq(trigger=Pin.IRQ_FALLING, handler=proximity_interrupt_handler)  
button_int_pin.irq(trigger=Pin.IRQ_FALLING, handler=button_interrupt_handler)


# main program loop
while True:

    # Check for change in flap position
    if change_in_flap_position == 1:

        if flap_position == 0:                           # flap was closed and got opened
            prox_sensor.interrupt_setup_open_state()     # configure the proximity sensor to send an interrupt if flap gets closed

            state = disable_irq()                        # disable interrupt requests to avoid concurrent access on shared objects 
            change_in_flap_position = 0                  # indicate that program handled change in flap position
            flap_position = 1                            # program indicates that flap is open
            enable_irq(state)                            # reenable interrupt requests

            print("New post")
            prox_sensor.interrupt_reset()                # reset interrupt status register

        else:                                            # flap was open and got closed long enough

            prox_sensor.interrupt_setup_closed_state()   # configure the proximity sensor to send an interrupt if flap gets opened

            state=disable_irq()                          # disable interrupt requests to avoid concurrent access on shared objects 
            change_in_flap_position = 0                  # indicate that program handled change in flap position
            flap_position = 0                            # program indicates that flap is closed
            closed_flap_counter = 0                      # reset flap counter
            enable_irq(state)                            # reenable interrupt requests

            print("The flap was closed again")
            prox_sensor.interrupt_reset()                # reset interrupt status register


    # Check if button got pressed
    if button_pressed == 1:

        if door_position == 0:                          # if door is closed

            alsData = VCNL4010_sensor.DATA_NOT_READY    # take ambient light reading
            while alsData == VCNL4010_sensor.DATA_NOT_READY :
                alsData = als_sensor.read_al()

            print("alsData:")
            print(alsData)
            if alsData < 200:                            # if it is too dark, light up LED
                led.value(True)

            while motor_position < DOOR_OPEN:            # open the door with the servomotor slowly
                servo.duty(motor_position)
                motor_position += 1
                time.sleep_ms(20)

            state=disable_irq()                          # disable interrupt requests to avoid concurrent access on shared objects
            button_pressed = 0                           # indicate that program handled button press
            enable_irq(state)                            # reenable interrupt requests

            door_position = 1                            # indicate that the door is open now

        else:                                            # if door is open

            while motor_position > DOOR_CLOSED:          # close door with the servomotor slowly
                servo.duty(motor_position)
                motor_position -= 1
                time.sleep_ms(20)

            led.value(False)                             # turn off LED anyways

            state=disable_irq()                          # disable interrupt requests to avoid concurrent access on shared objects
            button_pressed = 0                           # indicate that program handled button press
            enable_irq(state)                            # reenable interrupt requests

            door_position = 0                            # indicate that the door is open now

    time.sleep_ms(20)
