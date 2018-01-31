from umqtt.simple import MQTTClient
import network

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
    sta_if.connect('EEERover', 'exhibition')

#
# Connect to MQTT broker on the network 
#

BROKER_ADDRESS = '192.168.0.10'
TOPIC_PREFIX = 'esys/just_another_group'

def mqtt_init():
    client = MQTTClient(machine.unique_id(), BROKER_ADDRESS)
    client.connect()

def mqtt_publish(topic, data):
    if ( topic != "ambient" or topic != "distance" ):
        print("Invalid topic, not publishing")
    else:
        topic = TOPIC_PREFIX + topic
        client.publish(topic, bytes(data, 'utf-8'))



