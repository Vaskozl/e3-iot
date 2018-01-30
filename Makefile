
FILES = main

PORT=/tmp/usb-port


all: $(FILES) reset screen

$(PORT):
	ls /dev/tty* > /tmp/1; \
	echo "Detecting USB port, plug or unplug your controller now.\c"; \
	while [ -z $$USB ]; do \
		sleep 1; \
		echo ".\c"; \
		ls /dev/tty* > /tmp/2; \
		USB=`diff /tmp/1 /tmp/2 | grep -o '/dev/tty.*'`; \
	done; \
	echo ""; \
	echo "Detected controller on USB port at $$USB"; \
	sleep 1; \
	echo $$USB > $(PORT);

$(FILES): $(PORT) 
		echo "Uploading $@"; \
		ampy --port `cat $(PORT)` put $@.py;
	

screen: $(PORT)
	screen `cat $(PORT)` 115200

clean:
	if [ -f $(PORT) ]; then rm $(PORT); fi

reset:
		echo "Reseting"; \
		ampy --port `cat $(PORT)` reset;
