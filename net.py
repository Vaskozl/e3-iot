from umqtt.simple import MQTTClient
import network
import machine

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
        MQTTClient.__init__(self, machine.unique_id(), broker_address)
        print('machine_id:', machine.unique_id())
        print("Attempting to connect to broker");
        self.prefix = topic_prefix
    def send(self, sensor, value):
        if ( sensor != "ambient" and sensor != "proximity" ):
            print("Invalid topic, not publishing")
        else:
            topic = self.prefix + sensor
            MQTTClient.publish(self, topic, value)



