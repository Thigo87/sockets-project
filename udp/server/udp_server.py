import threading
from time import sleep, localtime
from core.json_manipulation import *
from server.models import Server

rooms = {}
active_ports = {}

def update_rooms(file):
    global rooms
    while True:
        try:
            current_rooms = read_data(file)
            if isinstance(current_rooms, dict):
                rooms = current_rooms
                
                for room_name, info in rooms.items():
                    port = int(info[1])
                    if port not in active_ports:
                        try:
                            server_obj = Server(room_name, port)
                            active_ports[port] = server_obj
                            t = threading.Thread(target=server_obj.receive_connection, daemon=True)
                            t.start()

                        except OSError as e:
                            print(f"It was not possible to open port {port} ({room_name}): {e}")
                            active_ports[port] = None
        
        except Exception as e:
            print(f"[{localtime().tm_hour}:{localtime().tm_min}:{localtime().tm_sec} - {localtime().tm_mday}/{localtime().tm_mon}/{localtime().tm_year}] An error occurred while reading JSON: {e}")
        
        sleep(0.1)

t2 = threading.Thread(target=update_rooms, args=("rooms.json",), daemon=True)
t2.start()

while True:
    sleep(1)
