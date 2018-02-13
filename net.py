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
            pass
    print('Connected to WiFi:', sta_if.ifconfig())

#
# Connect to MQTT broker on the network 
#

class Mqtt(MQTTClient):
    def __init__(self, broker_address, topic_prefix):
        MQTTClient.__init__(self, 'ee3-smartbox', broker_address)
        print("Attempting to connect to broker");
        self.prefix = topic_prefix
    def send(self, event, mail_count):
        if ( event != "NEW" and event != "DOOR" ):
            print("Invalid event, not publishing")
        else:
            print("Sending message");
            message = { "event": event, "mail_count": mail_count }
            MQTTClient.publish(self, self.prefix, ujson.dumps(message))



