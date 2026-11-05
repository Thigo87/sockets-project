from socket import *

serverName = "localhost"
dns_server_port = 12000
clientSocket = socket(AF_INET, SOCK_DGRAM)

option = input("Enter an option:\n[1] - Create a room\n[2] - Enter in a room\n[3] - Exit ")

while (addr != "1") or (addr != "2") or (addr != "3"):
    print("Enter a valid option!")
    addr = input("Enter an option:\n[1] - Create a room\n[2] - Enter in a room\n[3] - Exit ")

clientSocket.sendto(option.encode(), (serverName, dns_server_port))
response, serverAddress = clientSocket.recvfrom(2048)
print(response.decode())

ipAddr = response.decode().split(":")
ipAddr[1] = int(ipAddr[1])
print(ipAddr)

clientSocket.sendto("Hello".encode(), (ipAddr[0], ipAddr[1]))
response, serverAddress = clientSocket.recvfrom(2048)
print(response.decode())

clientSocket.close()