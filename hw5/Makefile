PORT = 8080
IP = 127.0.0.1
FILE = test.txt

tcp-server: TCP-server.py
	@python3 TCP-server.py $(PORT)

tcp-client: TCP-client.py check
	@python3 TCP-client.py $(IP) $(PORT) $(FILE)
	@make check

udp-server: UDP-server.py
	@python3 UDP-server.py $(PORT)

udp-client: UDP-client.py check
	@python3 UDP-client.py $(IP) $(PORT) $(FILE)
	@make check

clean:
	@rm -rf received_files

check:
	@echo "Checking for file consistency..."
	@diff $(FILE) received_files/$(FILE)
	@ORIGINAL_MD5=$$(md5sum $(FILE) | awk '{print $$1}') ; \
	RECEIVED_MD5=$$(md5sum received_files/$(FILE) | awk '{print $$1}') ; \
	if [ "$$ORIGINAL_MD5" != "$$RECEIVED_MD5" ]; then \
		echo "MD5 checksums differ:" ; \
		echo "Original:   $$ORIGINAL_MD5" ; \
		echo "Received:   $$RECEIVED_MD5" ; \
	fi ;
	@echo "File consistency check complete."

.PHONY: clean zip check