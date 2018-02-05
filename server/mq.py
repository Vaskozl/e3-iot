#!/usr/bin/python
import paho.mqtt.subscribe as subscribe

topics = ['esys/just_another_group/#']

m = subscribe.simple(topics, hostname="192.168.0.10", retained=False, msg_count=2)
for a in m:
    print(a.topic)
    print(a.payload)
