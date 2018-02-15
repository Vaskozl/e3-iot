# net.py: Implementation of the wireless functionalities

from umqtt.simple import MQTTClient
import network
import ujson

#
# Connect to test Wireless access Point 
#

def wpa_init():
    ap_if = network.WLAN(network.AP_IF)                              # construct access point interface
    ap_if.active(False)                                              # use it to disable access point functionality
    
    sta_if = network.WLAN(network.STA_IF)                            # construct wpa client interface
    sta_if.active(True)                                              # activate it
    if not sta_if.isconnected():                                     # check if already connected
        print('Attempting to authenticate with wireless network...') 
        sta_if.connect('EEERover', 'exhibition')                     # if not connect to EEERover network
        while not sta_if.isconnected():                              # Hang around untill we establish a connection
            pass 
    print('Connected to WiFi:', sta_if.ifconfig())

#
# Connect to MQTT broker on the network 
#

# We make an Mqtt class which wraps MQTTClient to simplify main.py calls

class Mqtt(MQTTClient):
    def __init__(self, broker_address, topic_prefix, serial_num):
        MQTTClient.__init__(self, 'ee3-smartbox', broker_address)      # establish connection with broker
        print("Attempting to connect to broker");
        self.prefix = topic_prefix                                     # set topic prefix
    def send(self, event, mail_count):                                 # make a simpler send func
        if ( event != "delivery" and event != "collection" ):          # check if event is valid
            print("Invalid event, not publishing")
        else:
            print("Sending message");
            message = { "mail_count": mail_count, "serial_id": serial_num}    # format JSON payload
            MQTTClient.publish(self, self.prefix+event, ujson.dumps(message)) # send message to correct channel based on event



