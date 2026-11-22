from socket import *
import threading
from random import randint
from clienttcp import recebe_linha

#estado de todas as salas abertas neste servidor
#salas["sala1"]={"tabuleiro":"123456789","vez":"X","jogadores":{id:{...}}}
salas={}

def novo_id(sala):
    id_jogador=str(randint(1000,9999))
    while id_jogador in sala["jogadores"]:
        id_jogador=str(randint(1000,9999))
    return id_jogador

def recusa(conn,motivo):
    conn.sendall(f"ERRO ; {motivo}\n".encode())
    conn.close()

def aceita_jogadores(sock_tcp,nome,sala):
    while True:
        conn,endereco=sock_tcp.accept()
        print(f"Conexao de {endereco[0]}:{endereco[1]}")

        jogador={"simbolo":"","socket":conn,"seq":0,"buffer":""}
        campos=recebe_linha(conn,jogador).split(" ; ")

        if campos[0]!="ENTRAR" or len(campos)<2 or campos[1]!=nome:
            recusa(conn,"sala errada")
            continue

        if len(sala["jogadores"])>=2:
            recusa(conn,"sala cheia")
            continue

        if len(sala["jogadores"])==0:
            jogador["simbolo"]="X"
        else:
            jogador["simbolo"]="O"

        id_jogador=novo_id(sala)
        sala["jogadores"][id_jogador]=jogador
        conn.sendall(f"BEMVINDO ; {id_jogador} ; {jogador['simbolo']}\n".encode())
        print(f"{id_jogador} entrou na {nome} como {jogador['simbolo']}")

def abre_sala(nome,porta):
    sala={"tabuleiro":"123456789","vez":"X","jogadores":{}}
    salas[nome]=sala

    sock_tcp=socket(AF_INET,SOCK_STREAM)
    sock_tcp.setsockopt(SOL_SOCKET,SO_REUSEADDR,1) #deixa reabrir a porta logo apos fechar o servidor
    sock_tcp.bind(("",porta))
    sock_tcp.listen(2)
    print(f"Sala {nome} esperando jogadores na porta {porta}")

    t_tcp=threading.Thread(target=aceita_jogadores,args=(sock_tcp,nome,sala))
    t_tcp.start()
    #a thread udp da sala (jogadas) entra aqui, na mesma porta, recebendo o mesmo dict sala
    return sala

if __name__=="__main__":
    #por enquanto uma sala fixa; depois vem do rooms.json
    abre_sala("sala1",12000)
