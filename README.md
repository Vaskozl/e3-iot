# SmartBox

This GitHub repository contains all the code for the implementation of the EE3 SmartBox project. The Box was demonstrated on 25/02/2018, developed by group VKPD. The embedded software was written in MicroPython, for the NodeMCU board.

Embedded code: main.py, net.py and VCNL4010.py
main.py: implements the controlling logic of the system as a whole
net.py: contains relevant MQTT and wireless functionalities
VCNL4010: contains the class for interfacing with the VCNL4010 infrared proximity sensor


The rest of the repository contains:
Makefile: a script created by us to make it easy to upload the embedded files to the NodeMCU board
webenv and Frontend folders: contain all the necessary files for the marketing and login website.

[Check out our webpage!](http://skozl.com:17318)

# Product 

SmartBox is the modern way to get your old-fashioned paper mail. Never miss your important letters again! Smartbox will let you know immediately when there is new mail!

## What is it all about?
You do not need to make everything smarter, but sometimes it just makes so much sense. 

￼
The internet brought big changes in the way we communicate with each other. Do you remember the last time you sent a mail (an actual, not an e-mail)? Me neither. I guess, you check your bank account online? Yes, that’s you. You absolutely hate unaddressed advertising and so you keep it away from your postbox. In the end, you almost never receive any post and eventually just stop checking your postbox, because you think there is really no point. But then it happens. Your friend from college sends you an invitation for his wedding. It stays unread in the postbox and you just miss the event. Your friend is mad and you are thinking:

### “Why did I not check my mails?”
No worries, we are here to help. Introducing SmartBox, the ideal solution to your problem. We developed a mailbox for the 21st century, that does not only simply look good, but also helps you to make your life simpler.

## Technical Details
* Two VCNL4010 sensors are utilised:
	*one for ambient light sensing
	* one for proximity measurement
* Sensor limitations: max. 20 cm distance and 16000 lux
* I2C communication with the processing unit
* Functions implemented using the ESP8266 board, interfaced through the NodeMCU board
* Size: H: 32 cm x W: 22 cm x D: 8 cm
* Weight: 1.6 kg
* Door opens with Tower pro SG92R servo motor
* Lamp: Power saving LED panel
* Solar charger unit
