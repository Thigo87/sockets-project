from socket import *
import threading
from random import randint
from clienttcp import recebe_linha

#estado de todas as salas abertas neste servidor
#salas["sala1"]={"tabuleiro":"123456789","vez":"X","jogadores":{id:{...}},"trava":Lock}
salas={}

def novo_id(sala):
    id_jogador=str(randint(1000,9999))
    while id_jogador in sala["jogadores"]:
        id_jogador=str(randint(1000,9999))
    return id_jogador

def enviar_um(sala,jogador,mensagem):
    #manda uma mensagem tcp para um jogador so (ex: INVALIDA)
    with sala["trava"]:
        jogador["socket"].sendall(f"{mensagem}\n".encode())

def enviar_todos(sala,mensagem):
    #manda a mesma mensagem tcp para todos os jogadores da sala (ex: TABULEIRO, FIM)
    with sala["trava"]:
        for jogador in sala["jogadores"].values():
            jogador["socket"].sendall(f"{mensagem}\n".encode())

def mensagem_tabuleiro(sala):
    return f"TABULEIRO ; {sala['tabuleiro']} ; {sala['vez']}"

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

        if len(sala["jogadores"])==2:
            print(f"Sala {nome} cheia, comecando o jogo")
            enviar_todos(sala,mensagem_tabuleiro(sala))

def abre_sala(nome,porta):
    #a trava evita que duas threads escrevam no mesmo socket ao mesmo tempo
    sala={"tabuleiro":"123456789","vez":"X","jogadores":{},"trava":threading.Lock()}
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
