from socket import *
import threading
import time
#DEFINE n=500

def escuta_tcp(ip,porta):
    s=socket(AF_INET,SOCK_STREAM)
    s.connect((ip,porta))
    reposta=s.recv(n)
    
    while(reposta.decode()!="fim"):
        print(reposta.decode())
        reposta=s.recv(n) #talvez mandar pro txt
    #avisa pro que acabou o jogo no txt e fecha a conexao
    s.close()

def tcp_client():
    ip=input("Digite o IP do servidor: ")
    porta=int(input("Digite a porta do servidor: "))
    t1=threading.Thread(target=escuta_tcp,args=(ip,porta))
    t1.start()
    time.sleep(1)
    se=socket(AF_INET,SOCK_STREAM)
    se.connect((ip,porta))
    sala=input("Digite a sala que deseja entrar: ")
    se.send(sala.encode())
    #inicia a funçao do jogo t2 que le o txt para prencher e faz envios quando for a vez 
    #t1.join()
    # t2..join  
    
