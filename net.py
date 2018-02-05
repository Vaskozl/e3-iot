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



