from socket import *
from time import sleep

serverName = "localhost"
dns_server_port = 10000


while True:
    clientSocket = socket(AF_INET, SOCK_DGRAM)
    option = input("Enter an option:\n[1] - Create a room\n[2] - Enter in a room\n[3] - View available rooms\n[4] - Delete a room\n[5] - Exit\nEnter an option: ")

    while (option != "1") and (option != "2") and (option != "3") and (option != "4") and (option != "5"):
        print("Enter a valid option!")
        option = input("Enter an option:\n[1] - Create a room\n[2] - Enter in a room\n[3] - View available rooms\n[4] - Delete a room\n[5] - Exit\nEnter an option: ")

    if option != "5":
        msg = ""
        room_name = ""
        if option == "1":
            room_name = input("Enter the name of the room you want to create: ")
            
        elif option == "2":
            room_name = input("Enter the name of the room you want to join: ")
            
        elif option == "4":
            room_name = input("Enter the name of the room you want to delete: ")

        msg += f"{room_name} ; {option}"
        clientSocket.sendto(msg.encode(), (serverName, dns_server_port))
        response, serverAddress = clientSocket.recvfrom(2048)

        if option != "3" and option != "4":
            ipAddr = response.decode().split(":")
            ipAddr[1] = int(ipAddr[1])

            if ipAddr[1] == 0: #error or a message from the dns server
                print(ipAddr[0])
            else:
                print(ipAddr)
                               
                clientSocket.settimeout(1)
                connected = False
                
                for _ in range(3):
                    try:
                        clientSocket.sendto("Hello".encode(), (ipAddr[0], ipAddr[1]))
                        response, serverAddress = clientSocket.recvfrom(2048)
                        print(response.decode())
                        connected = True
                        break
                    
                    except (ConnectionResetError, TimeoutError):
                        sleep(0.3)
                        
                if not connected:
                    print("Failed to connect to the server.")
                        

        else:
            if option == "3":
                msg_received = response.decode().split(" : ")

                print("\n====AVAILABLE ROOMS====")

                for r in msg_received:
                    print(f"- {r}")

            else:
                msg_received = response.decode().split(":")[0]
                print(msg_received)
                
        clientSocket.close()

        print("")
        
    else:
        print("Bye!")
        break
