from socket import *
import threading
n=1024

def mostra_tabuleiro(tabuleiro):
    for i in range(0,9,3):
        print(f" {tabuleiro[i]} | {tabuleiro[i+1]} | {tabuleiro[i+2]}")
        if i<6:
            print("-----------")

def recebe_linha(sock,estado):
    #junta os pedaços do recv ate ter uma mensagem inteira (termina com \n)
    while "\n" not in estado["buffer"]:
        dado=sock.recv(n)
        if not dado:
            return ""
        estado["buffer"]+=dado.decode()
    linha,_,estado["buffer"]=estado["buffer"].partition("\n")
    return linha

def escuta_tcp(sock,estado):
    while not estado["fim"]:
        linha=recebe_linha(sock,estado)
        if linha=="":
            print("Conexao com o servidor perdida")
            estado["fim"]=True
            break

        campos=linha.split(" ; ")
        tipo=campos[0]

        if tipo=="TABULEIRO":
            estado["tabuleiro"]=campos[1]
            estado["vez"]=campos[2]
            mostra_tabuleiro(estado["tabuleiro"])
            if estado["vez"]==estado["simbolo"]:
                print("Sua vez!")
                estado["minha_vez"]=True
            else:
                print(f"Vez do {estado['vez']}")
            estado["chegou_resposta"]=True

        elif tipo=="INVALIDA":
            print(f"Jogada invalida: {campos[2]}")
            estado["minha_vez"]=True
            estado["chegou_resposta"]=True

        elif tipo=="FIM":
            resultado=campos[1]
            if resultado=="EMPATE":
                print("Deu velha!")
            elif resultado=="DESISTENCIA":
                print("O outro jogador saiu. Voce venceu!")
            elif resultado==estado["simbolo"]:
                print("Voce venceu!")
            else:
                print("Voce perdeu!")
            estado["fim"]=True

    sock.close()

def tcp_client(ip,porta,sala):
    estado={"id":"","simbolo":"","tabuleiro":"123456789","vez":"",
            "minha_vez":False,"chegou_resposta":False,"fim":False,"buffer":""}

    se=socket(AF_INET,SOCK_STREAM)
    se.connect((ip,porta))
    se.sendall(f"ENTRAR ; {sala}\n".encode())

    campos=recebe_linha(se,estado).split(" ; ")
    if campos[0]=="BEMVINDO":
        estado["id"]=campos[1]
        estado["simbolo"]=campos[2]
        print(f"Voce e o {estado['simbolo']}. Esperando o outro jogador...")
    else:
        if len(campos)>1:
            print(campos[1])
        else:
            print("Erro ao entrar na sala")
        se.close()
        return None,None

    t1=threading.Thread(target=escuta_tcp,args=(se,estado))
    t1.start()
    #a t2 (jogadas por udp) entra aqui, usando estado["id"] e estado["minha_vez"]
    return estado,t1

if __name__=="__main__":
    #por enquanto fixo; depois vem da resposta do dns
    estado,t1=tcp_client("localhost",12000,"sala1")
    if t1:
        t1.join()
