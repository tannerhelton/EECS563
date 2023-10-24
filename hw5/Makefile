PORT = 8080
IP = 127.0.0.1
FILE = test.txt

server: TCP-server.py
	@python3 TCP-server.py $(PORT)

client: TCP-client.py
	@python3 TCP-client.py $(IP) $(PORT) $(FILE)

clean:
	@rm -rf received_files