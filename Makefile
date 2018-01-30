MAKEFLAGS += --silent

FILES = main.py

PORT=/tmp/usb-port

$(PORT):
	ls /dev/tty* > /tmp/1; \
	echo "Detecting USB port, plug your controller now.\c"; \
	while [ -z $$USB ]; do \
		sleep 1; \
		echo ".\c"; \
		ls /dev/tty* > /tmp/2; \
		USB=`diff /tmp/1 /tmp/2 | grep -o '/dev/tty.*'`; \
	done; \
	echo ""; \
	echo "Detected controller on USB port at $$USB"; \
	echo $$USB > $(PORT);
	sleep 1;

%.py: $(PORT)
		echo "Uploading $@"; \
		ampy --port `cat $(PORT)` put $@;
	
all: $(FILES)

screen: $(PORT)
	screen `cat $(PORT)` 115200

reset: $(PORT)
		echo "Reseting" \
		ampy --port `cat $(PORT)` reset

clean:
	if [ -f $(PORT) ]; then rm $(PORT); fi
