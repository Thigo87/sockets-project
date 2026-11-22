from socket import *
import threading
from json_manipulation import *
from time import sleep

data = ""

def read(file):
    global data
    while True:
        data = read_data(file)
        sleep(1)

def write():
    print(data)

t1 = threading.Thread(target=read, args=("rooms.json",))
t1.start()

while True:
    write()
    sleep(1)