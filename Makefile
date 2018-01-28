MAKEFLAGS += --silent

FILES = main.py test.py

PORT=/tmp/usb-port

$(PORT):
	ls /dev/tty* > /tmp/1; \
	echo "Detecting USB port, reset your controller now.\c"; \
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

%.py: $(PORT)
		echo "Uploading $@"; \
		ampy --port `cat $(PORT)` put $@;
	
all: $(FILES)

clean:
	if [ -f $(PORT) ]; then rm $(PORT); fi
