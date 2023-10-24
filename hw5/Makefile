PORT = 8080
IP = 127.0.0.1
FILE = test.txt

tcp-server: TCP-server.py
	@python3 TCP-server.py $(PORT)

tcp-client: TCP-client.py
	@python3 TCP-client.py $(IP) $(PORT) $(FILE)

udp-server: UDP-server.py
	@python3 UDP-server.py $(PORT)

udp-client: UDP-client.py
	@python3 UDP-client.py $(IP) $(PORT) $(FILE)

clean:
	@rm -rf received_files

.PHONY: clean