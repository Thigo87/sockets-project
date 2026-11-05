from socket import *
import threading
import json

dados = {"as" : ["localhost", "12500"]}
arquivo = open("./udp/rooms.json", "w")
#ver como adiciona elemento sem excluir tudo
json.dump(dados, arquivo)
arquivo.close()

arquivo = open("./udp/rooms.json", "r")
data = json.load(arquivo)
arquivo.close()
print(data)