# net.py: Implementation of the wireless functionalities

from umqtt.simple import MQTTClient
import network
import ujson

#
# Connect to test Wireless access Point 
#

def wpa_init():
    # Disable being an AP
    ap_if = network.WLAN(network.AP_IF)
    ap_if.active(False)
    
    # Connect to Test AP
    sta_if = network.WLAN(network.STA_IF)
    sta_if.active(True)
    if not sta_if.isconnected():
        print('Attempting to authenticate with wireless network...')
        sta_if.connect('EEERover', 'exhibition')
        while not sta_if.isconnected():
            pass # Hang around until we establish a connection
    print('Connected to WiFi:', sta_if.ifconfig())

#
# Connect to MQTT broker on the network 
#

class Mqtt(MQTTClient):
    def __init__(self, broker_address, topic_prefix, serial_num):
        MQTTClient.__init__(self, 'ee3-smartbox', '192.168.0.10')      # establish connection with broker
        print("Attempting to connect to broker");
        self.prefix = topic_prefix                                     # set topic prefix
    def send(self, event, mail_count):
        if ( event != "delivery" and event != "collection" ):          # check if event is valid
            print("Invalid event, not publishing")
        else:
            print("Sending message");
            message = { "mail_count": mail_count, "serial_id": serial_num} # format JSON payload
            MQTTClient.publish(self, self.prefix+event, ujson.dumps(message))



