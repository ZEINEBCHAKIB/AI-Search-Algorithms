import math 

"""Constantes et initialisation"""
PLAYER_X = 'X'  # Joueur humain
PLAYER_0 = 'O'  # IA
EMPTY = '.'      # Case vide

""" Affichage du plateau de jeu dans la console."""
def print_board(board):
    for row in board:
        print("|".join(row))
    print("-" * 5)
    
""" Vérification si la partie est terminée"""
def is_game_over(board):
    # Vérifie les lignes, colonnes et diagonales
    for row in board:
        if row.count(row[0]) == 3 and row[0] != EMPTY:
            return True
    for col in range(3):
        if board[0][col] == board[1][col] == board[2][col] != EMPTY:
            return True
    if (board[0][0] == board[1][1] == board[2][2] != EMPTY) or (board[0][2] == board[1][1] == board[2][0] != EMPTY):
        return True
    if all(cell != EMPTY for row in board for cell in row):
        return True  # Match nul
    return False

"""Évaluation du plateau et attribution d'un score"""
def evaluate_board(board):
    # Vérifie les victoires ou match nul
    for row in board:
        if row.count(PLAYER_0) == 3:
            return 1 
        if row.count(PLAYER_X) == 3:
            return -1
    for col in range(3):
        if (board[0][col] == board[1][col] == board[2][col]) and board[0][col] != EMPTY:
            return 1 if board[0][col] == PLAYER_0 else -1
    if (board[0][0] == board[1][1] == board[2][2] != EMPTY):
        return 1 if board[1][1] == PLAYER_0 else -1
    if (board[0][2] == board[1][1] == board[2][0] != EMPTY):
        return 1 if board[1][1] == PLAYER_0 else -1
    return 0  # Match nul ou partie en cours

"""Implémentation d'algorithme Minimax pour évaluer récursivement les coups possibles"""
def minimax(board, depth, is_maximizing):
    if is_game_over(board):
        return evaluate_board(board)
    if is_maximizing:
        best_score = -math.inf
        for i in range(3):
            for j in range(3):
                if board[i][j] == EMPTY:
                    board[i][j] = PLAYER_0
                    score = minimax(board, depth + 1, False)
                    board[i][j] = EMPTY
                    best_score = max(score, best_score)
        return best_score
    else:
        best_score = math.inf
        for i in range(3):
            for j in range(3):
                if board[i][j] == EMPTY:
                    board[i][j] = PLAYER_X
                    score = minimax(board, depth + 1, True)
                    board[i][j] = EMPTY
                    best_score = min(score, best_score)
        return best_score
    
"""Utilisation minimax() pour trouver le meilleur coup pour l'agent ia """
def find_best_move(board):
    best_score = -math.inf
    move = (-1, -1)
    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY:
                board[i][j] = PLAYER_0
                score = minimax(board, 0, False)
                board[i][j] = EMPTY
                if score > best_score:
                    best_score = score
                    move = (i, j)
    return move

"""Fonction Principale"""
def main():
    board = [[EMPTY for _ in range(3)] for _ in range(3)]
    print("Welcome to Tic-Tac-Toe!")
    print_board(board)
    while not is_game_over(board):
        # Tour du joueur humain (X)
        while True:
            try:
                x, y = map(int, input("Enter your move (row and column): ").split())
                if board[x][y] == EMPTY:
                    board[x][y] = PLAYER_X
                    break
                else:
                    print("Cell is already occupied! Try again.")
            except (ValueError, IndexError):
                print("Invalid input! Please enter row and column as two numbers (0, 1, or 2).")
        print_board(board)
        if is_game_over(board):
            break
        # Tour de l'IA (O)
        print("Computer's turn:")
        move = find_best_move(board)
        if move != (-1, -1):
            board[move[0]][move[1]] = PLAYER_0
        print_board(board)
    # Résultat final
    if evaluate_board(board) == 1:
        print("Computer (O) wins!")
    elif evaluate_board(board) == -1:
        print("You (X) win!")
    else:
        print("It's a draw!")

main()

