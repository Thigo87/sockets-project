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
    coluna1 = [board[0][1], board[1][1], board[2][1]]
    coluna2 = [board[0][2], board[1][2], board[2][2]]
    
    print(coluna0)
    print(coluna1)
    print(coluna2)

    if diagonal1 == ["O", "O", "O"] or diagonal2 == ["O", "O", "O"]:
        winner = ["O", True]
    elif diagonal1 == ["X", "X", "X"] or diagonal2 == ["X", "X", "X"]:    
        winner = ["X", True]
    
    if coluna0 == ["O", "O", "O"] or coluna1 == ["O", "O", "O"] or coluna2 == ["O", "O", "O"]:
            winner = ["O", True]
    elif coluna0 == ["X", "X", "X"] or coluna1 == ["X", "X", "X"] or coluna2 == ["X", "X", "X"]:    
        winner = ["X", True]
            
    return winner

board = [["O", "2", "3"], ["O", "5", "6"], ["O", "8", "9"]]

print(win(board))