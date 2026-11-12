from socket import *
import threading
from json_manipulation import *
import time

rooms = read_data()

def receive_connection(port):
    serverUDP = socket(AF_INET, SOCK_DGRAM)
    serverUDP.bind(("", port))
    print(f"Server localhost:{port} is ready to receive")

    message, address = serverUDP.recvfrom(2048) #ajustar a quantidade de bits

    message = message.decode()
    print(f"Received message: {message}\nFrom: {address[0]}:{address[1]}")

    serverUDP.sendto("Message received!".encode(), address)

    serverUDP.close()

for room in rooms:
    t = threading.Thread(target=receive_connection, args=(int(rooms[room][1]),))
    t.start()

#ajustar pra atualizar as salas disponíveis em tempo real