from socket import *
import threading
from json_manipulation import *
from time import sleep

def read(file):
    while True:
        print(read_data(file))
        sleep(1)

t = threading.Thread(target=read, args=("rooms.json",))
t.start()
