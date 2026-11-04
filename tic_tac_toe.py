import os
import subprocess
from random import randint
from time import sleep

def showBoard(board):
    counter = 0
    for line in board:
        line_to_present = ""
        counter2 = 0
        for item in line:
            counter2 += 1
            if counter2 < 3:
                line_to_present += f" {item} |"
            else:
                line_to_present += f" {item}"
        print(line_to_present)
        counter += 1
        if counter < 3:
            print("------------")

def win(board):
    winner = ["", False]
    #verifing lines
    for line in board:
        if not winner[1]:
            if line == ["O", "O", "O"]:
                winner = ["O", True]
            elif line == ["X", "X", "X"]:
                winner = ["X", True]
    
    diagonal1 = [board[0][0], board[1][1], board[2][2]]
    diagonal2 = [board[0][2], board[1][1], board[2][0]]
    
    #ajustar só a verificação das colunas
    coluna0 = [board[0][0], board[1][0], board[2][0]]
    coluna1 = [board[1][0], board[1][1], board[1][2]]
    coluna2 = [board[2][0], board[2][1], board[2][2]]
    
    if diagonal1 == ["O", "O", "O"] or diagonal2 == ["O", "O", "O"]:
        winner = ["O", True]
    elif diagonal1 == ["X", "X", "X"] or diagonal2 == ["X", "X", "X"]:    
        winner = ["X", True]
    
    if coluna0 == ["O", "O", "O"] or coluna1 == ["O", "O", "O"] or coluna2 == ["O", "O", "O"]:
            winner = ["O", True]
    elif coluna0 == ["X", "X", "X"] or coluna1 == ["X", "X", "X"] or coluna2 == ["X", "X", "X"]:    
        winner = ["X", True]
            
    return winner
           
def tie(board):
    tie = False
    counter = 0
    for line in board:
        for item in line:
            if item.isnumeric():
                counter += 1
    
    if counter == 0:
        tie = True
    
    return tie

def game(board, played):
    subprocess.run('cls' if os.name == 'nt' else 'clear', shell=True)
    player = ""
    if not win(board)[1]:
        showBoard(board)
        if played == "O":
            player = "X"
            x = input("Please input a number for X position: ")
            counter = 0
            for i in range(3):
                for j in range(3):
                    if board[i][j] == x:
                        board[i][j] = "X"
                        counter = 1
            
            if counter != 1:
                print("Invalid position! Next player.")
            
        else:
            player = "O"
            o = input("Please input a number for O position: ")
            counter = 0
            for i in range(3):
                for j in range(3):
                    if board[i][j] == o:
                        print(board[i][j])
                        board[i][j] = "O"
                        counter = 1
            
            if counter != 1:
                print("Invalid position! Next player.")
                sleep(1.5)
        
        conclusion = win(board)
           
        if not conclusion[1] and not tie(board):
            game(board, player)
        else:
            subprocess.run('cls' if os.name == 'nt' else 'clear', shell=True)
            showBoard(board)
            if not tie(board):
                print(f"{conclusion[0]} wins!")
            else:
                print("IT'S A TIE!")
        
board = [["1", "2", "3"], ["4", "5", "6"], ["7", "8", "9"]]
start_piece = randint(0, 1)
if start_piece == 0:
    print("'O' will start!")
    sleep(1.5)
    game(board, "X")
else:
    print("'X' will start!")
    sleep(1.5)
    game(board, "O")