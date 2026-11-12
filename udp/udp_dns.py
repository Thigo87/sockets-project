from socket import *
import threading
from json_manipulation import *
from random import randint

names = {'1' : ['localhost', '12500']}

serverName = "localhost"
dnsPort = 12000
dnsSocket = socket(AF_INET, SOCK_DGRAM)

dnsSocket.bind(("", dnsPort))
print("Nameserver ready!")
msg, returnAddr = dnsSocket.recvfrom(2048)
msg = msg.decode()
rooms = read_data()
used_ports = []

for room in rooms:
    used_ports.append(int(rooms[room][1]))

print(used_ports)
room_name, option = msg.split(" ; ")
print(room_name, option)

return_msg = ""

if room_name not in rooms:
    if option == "1":
        port = randint(10000, 99999)
        while port in used_ports:
            port = randint(10000, 99999)
        add_data({room_name : ["localhost", str(port)]})

else:
    if option == "2":
        pass
    else:
        return_msg = "This room already exists!"

#ajustar o retorno pro client

#print(f"Received name: {name}\nFrom: {returnAddr[0]}:{returnAddr[1]}")
#ipAddr = ""
#for n in names:
#    if n == name:
#        ipAddr = names[n][0] + ":" + names[n][1]
#print(f"Returning address {ipAddr} for {name} to {returnAddr[0]}:{returnAddr[1]}")
dnsSocket.sendto(return_msg.encode(), returnAddr)

dnsSocket.close()