from socket import *

serverName = "localhost"
dns_server_port = 12000
clientSocket = socket(AF_INET, SOCK_DGRAM)

addr = input("Enter the address: ")

clientSocket.sendto(addr.encode(), (serverName, dns_server_port))
response, serverAddress = clientSocket.recvfrom(2048)
print(response.decode())

ipAddr = response.decode().split(":")
ipAddr[1] = int(ipAddr[1])
print(ipAddr)

clientSocket.sendto("Hello".encode(), (ipAddr[0], ipAddr[1]))
response, serverAddress = clientSocket.recvfrom(2048)
print(response.decode())

clientSocket.close()