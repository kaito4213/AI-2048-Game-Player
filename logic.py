# All the move have three steps,  first move them, 
#                                 second find if there are same numbers, add them up
#                                 third move them 

from utils import *

def move_up(board):
    """
    Simulate a move up
    """
    pass

def move_down(board):
    pass

def move_left(board):
    pass

def move_right(board):
    pass


def move(board, action):
    """
    move the board based on action
    """
    N = len(board)
    if action == "UP":
        for col in range(0,N):
            firstEmpty = 0
            for j in range(0,N):
                if board[j][col] != '*':
                    swap(board, (j, col), (firstEmpty, col))
                    firstEmpty += 1
    
    if action == "DOWN":
        for col in range(0,N):
            firstEmpty = N-1
            for j in range(0,N):
                if board[N-1-j][col] != '*':
                    swap(board, (N-1-j, col), (firstEmpty, col))
                    firstEmpty -= 1

    if action == "LEFT":
        for row in range(0,N):
            firstEmpty = 0
            for j in range(0, N):
                if board[row][j] != '*':
                    swap(board, (row, j), (row, firstEmpty))
                    firstEmpty += 1
    
    if action == "RIGHT":
        for row in range(0,N):
            firstEmpty = N-1
            for j in range(0, N):
                if board[row][N-1-j] != '*':
                    swap(board, (row, N-1-j), (row, firstEmpty))
                    firstEmpty -= 1


def add_up(board, action, curr_score):
    """
    After each move, we need to add up the same elem
    """    
    new_score = curr_score
    N = len(board)
    if action == "UP":
        for col in range(0,N):
            for j in range(0, N-1):
                if board[j][col] == board[j+1][col] and board[j][col] != '*':
                    new_score += 2 * board[j][col]
                    board[j][col] = board[j][col] + board[j+1][col]
                    board[j+1][col] = '*'

    if action == "DOWN":
        for col in range(0,N):
            j = N-1
            while j > 0:
                if board[j][col] == board[j-1][col] and board[j][col] != '*':
                    new_score += 2 * board[j][col]
                    board[j][col] = board[j][col] + board[j-1][col]
                    board[j-1][col] = '*'
                j -= 1

            # for j in range(0, N-1):
            #     if board[N-1-j][col] == board[N-j][col]:
            #         board[N-1-j][col] = board[N-1-j][col] + board[N-j][col]
            #         board[N-j][col] = '*'

    if action == "LEFT":
        for row in range(0, N):
            for j in range(0, N-1):
                if board[row][j] == board[row][j+1] and board[row][j] != '*':
                    new_score += 2 * board[row][j]
                    board[row][j] = board[row][j] + board[row][j+1]
                    board[row][j+1] = '*'

    if action == "RIGHT":
        for row in range(0,N):
            j = N-1
            while j > 0:
                if board[row][j] == board[row][j-1] and board[row][j] != '*':
                    new_score += 2 * board[row][j]
                    board[row][j] = board[row][j] + board[row][j-1]
                    board[row][j-1] = '*'
                j -= 1

    return new_score
            # for j in range(0,N-1):
            #     if board[row][N-1-j] == board[row][N-j]:
            #         board[row][N-1-j] = board[row][N-1-j] + board[row][N-j]
            #         board[row][N-j] = '*'

def can_move(board, action):
    """
    Check if can make a move based on action 
    """
    N = len(board)
    if action == "UP":
        for col in range(0,N):
            j = 0
            while j < N and board[j][col] != '*':
                j += 1
            for k in range(j + 1, N):
                if board[k][col] != None and board[k][col] != '*':
                    return True

        for col in range(0, N):
            for j in range(0, N-1):
                if board[j][col] == board[j+1][col] and board[j][col] != '*':
                    return True
    
    if action == "DOWN":
        for col in range(0, N):
            j = N-1
            while j >=0 and board[j][col] != '*':
                j -= 1
            for k in range(0, j):
                if board[k][col] != None and board[k][col] != '*':
                    return True
        
        for col in range(0, N):
            j = N-1
            while j > 0:
                if board[j][col] == board[j-1][col] and board[j][col] != '*':
                    return True
                j -= 1
        
    
    if action == "LEFT":
        for row in range(0,N):
            j = 0
            while j < N and board[row][j] != '*':
                j += 1
            for k in range(j+1,N):
                if board[row][k] != None and board[row][k] != '*':
                    return True
        
        for row in range(0, N):
            for j in range(0,N-1):
                if board[row][j] == board[row][j+1] and board[row][j] != '*':
                    return True

    if action == "RIGHT":
        for row in range(0,N):
            j = N-1
            while j >= 0 and board[row][j] != '*':
                j -= 1
            for k in range(0, j):
                if board[row][j] != None and board[row][k] != '*':
                    return True

        for row in range(0, N):
            j = N-1
            while j > 0:
                if board[row][j] == board[row][j-1] and board[row][j] != '*':
                    return True
                j -= 1

    return False
