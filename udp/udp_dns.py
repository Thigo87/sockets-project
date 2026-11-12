from socket import *
import threading
from json_manipulation import *
from random import randint

def connection():
    dnsPort = 10000
    dnsSocket = socket(AF_INET, SOCK_DGRAM)

    dnsSocket.bind(("", dnsPort))
    print("Nameserver ready!")
    msg, returnAddr = dnsSocket.recvfrom(2048)
    print(f"Connected to: {returnAddr[0]}:{returnAddr[1]}")
    msg = msg.decode()
    rooms = read_data()
    used_ports = []

    for room in rooms:
        used_ports.append(int(rooms[room][1]))
    
    room_name, option = msg.split(" ; ")

    return_msg = ""

    if option == "1":
        if room_name not in rooms:
            port = randint(10002, 65535)
            while port in used_ports:
                port = randint(10002, 99999)
            add_data({room_name : ["localhost", str(port)]})
            return_msg = f"localhost:{port}"
        else:
            return_msg = "This room already exists!:0"

    elif option == "2":
        if room_name not in rooms:
            return_msg = "This room doesn't exists!:0"
        else:
            return_msg = f"{rooms[room_name][0]}:{rooms[room_name][1]}"

    elif option == "3":
        available_rooms = ""

        for r in read_data():
            available_rooms += f"{r} : "

        return_msg = available_rooms[:(len(available_rooms) - 3)]

    print(f"Message sent => {return_msg}")
    dnsSocket.sendto(return_msg.encode(), returnAddr)

    dnsSocket.close()

while True:
    connection()

