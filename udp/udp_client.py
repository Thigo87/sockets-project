from socket import *

serverName = "localhost"
dns_server_port = 12000
clientSocket = socket(AF_INET, SOCK_DGRAM)

option = input("[1] - Create a room\n[2] - Enter in a room\n[3] - Exit\nEnter an option: ")

while (option != "1") and (option != "2") and (option != "3"):
    print("Enter a valid option!")
    option = input("Enter an option:\n[1] - Create a room\n[2] - Enter in a room\n[3] - Exit\n")

if option != "3":
    msg = ""
    room_name = ""
    if option == "1":
        room_name = input("Enter the name of the room you want to create: ")
        
    elif option == "2":
        room_name = input("Enter the name of the room you want to join: ")

    msg += f"{room_name} ; {option}"
    clientSocket.sendto(msg.encode(), (serverName, dns_server_port))
    response, serverAddress = clientSocket.recvfrom(2048)
    print(response.decode())

    ipAddr = response.decode().split(":")
    print(ipAddr)
    ipAddr[1] = int(ipAddr[1])
    print(ipAddr)

    clientSocket.sendto("Hello".encode(), (ipAddr[0], ipAddr[1]))
    response, serverAddress = clientSocket.recvfrom(2048)
    print(response.decode())

    clientSocket.close()

else:
    print("Bye!")