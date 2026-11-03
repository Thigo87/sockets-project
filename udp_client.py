from socket import *

serverName = "localhost"
serverPort = 12000
clientSocket = socket(AF_INET, SOCK_DGRAM)

message = input("Enter your message: ")

clientSocket.sendto(message.encode(), (serverName, serverPort))
response, serverAddress = clientSocket.recvfrom(2048)
print(response.decode())

clientSocket.close()