from socket import *
import threading
import time
#DEFINE n=500

def escuta_tcp(sock,estado):
    
    while(not estado["fim"]):
        resposta=se.recv(n)
        resposta = se.recv(n)                       
        campos = resposta.decode().strip().split(" ; ")

        tipo = campos[0]
        if tipo == "TABULEIRO":
            estado["jogo"] = campos[1]
            estado["simbolo"] = campos[2]
        elif tipo == "ERRO":
            print(campos[1])
        
    
    s.close()

(estado = {"id": "", "simbolo": ""})

time.sleep(1)
se=socket(AF_INET,SOCK_STREAM)
se.connect((ip,porta))
se.send(f"ENTRAR ; {sala}\n".encode())
resposta=se.recv(n)
resposta = se.recv(n)                       
campos = resposta.decode().strip().split(" ; ")
# campos == ["BEMVINDO", "4821", "X"]
tipo = campos[0]
if tipo == "BEMVINDO":
    estado["id"] = campos[1]
    estado["simbolo"] = campos[2]
elif tipo == "ERRO":
    print(campos[1])
    se.close()
