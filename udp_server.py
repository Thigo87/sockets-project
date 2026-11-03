from socket import *
import threading

server_port = 12000

serverUDP = socket(AF_INET, SOCK_DGRAM)

serverUDP.bind(("", server_port))
print("Server is ready to receive")

message, address = serverUDP.recvfrom(2048) #ajustar a quantidade de bits

message = message.decode()
print(f"Received message: {message}\nFrom: {address[0]}:{address[1]}")

serverUDP.sendto("Message received!".encode(), address)

serverUDP.close()