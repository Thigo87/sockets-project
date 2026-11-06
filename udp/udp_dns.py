from socket import *
import threading

#names = open("rooms.txt", "w+")

names = {'1' : ['localhost', '12500']}

serverName = "localhost"
dnsPort = 12000
dnsSocket = socket(AF_INET, SOCK_DGRAM)

dnsSocket.bind(("", dnsPort))
print("Nameserver ready!")
name, returnAddr = dnsSocket.recvfrom(2048)
name = name.decode()
print(name)
print(f"Received name: {name}\nFrom: {returnAddr[0]}:{returnAddr[1]}")
ipAddr = ""
for n in names:
    if n == name:
        ipAddr = names[n][0] + ":" + names[n][1]
print(f"Returning address {ipAddr} for {name} to {returnAddr[0]}:{returnAddr[1]}")
dnsSocket.sendto(ipAddr.encode(), returnAddr)

dnsSocket.close()