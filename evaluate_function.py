# different kinds of evaluations
# May be used in different heuristic functions

import math

def smoothness(board):
    """
    measures how smooth the grid is 
    Sums of the pairwise difference between neighboring tiles (in log space, so it represents the
    number of merges that need to happen before they can merge). 
    """

    N = len(board)
    res = 0
    for i in range(N):
        for j in range(N):
            if board[i][j] != '*':
                curr_value = math.log(2,board[i][j])
                for direction in ('RIGHT', 'DOWN'):
                    next_num_cell = find_first_non_empty_cell(board, i,j, direction)
                    if next_num_cell != None:
                        x, y = next_num_cell
                        next_num_value = math.log(2,board[x][y])
                        res -= abs(curr_value - next_num_value)
    return res


def monotonicity(board):
    """
    measure the monotonicity of the board
    """

    N = len(board)

    # score[0]: up/down direction, increasing
    # score[1]: up/down direction, decreasing
    # score[2]: left/right direction, increasing
    # score[3]: left/right direction, decreasing
    score = [0,0,0,0]

    # up/down direction
    for row in range(N):
        curr_cell = 0
        while curr_cell < N and board[row][curr_cell] == '*':
            curr_cell += 1
        next_cell = curr_cell + 1
        while next_cell < N:
            while next_cell < N and board[row][next_cell] == '*':
                next_cell += 1

            if next_cell < N:
                if board[row][curr_cell] > board[row][next_cell]:
                    score[0] += board[row][next_cell] - board[row][curr_cell]
                elif board[row][curr_cell] < board[row][next_cell]:
                    score[1] += board[row][curr_cell] - board[row][next_cell]
            
            curr_cell = next_cell
            next_cell += 1
    
    # left/right direction
    for col in range(N):
        curr_cell = 0
        while curr_cell < N and board[curr_cell][col] == '*':
            curr_cell += 1
        next_cell = curr_cell + 1
        while next_cell < N:
            while next_cell < N and board[next_cell][col] == '*':
                next_cell += 1

            if next_cell < N:
                if board[curr_cell][col] > board[next_cell][col]:
                    score[2] += board[next_cell][col] - board[curr_cell][col]
                elif board[curr_cell][col] < board[next_cell][col]:
                    score[3] += board[curr_cell][col] - board[next_cell][col]
            
            curr_cell = next_cell
            next_cell += 1

    return max(score[0], score[1]) + max(score[2],score[3])


def emptiness(board):
    """
    measure how empty the board is
    simply return the number of empty board
    """
    N = len(board)
    
    count = 0
    for i in range(N):
        for j in range(N):
            if board[i][j] == '*':
                count += 1
    return count

def max_val(board):
    """
    find the max value of the board

    Duplicate with utils.find_max_cell
    """
    N = len(board)
    res = 0
    for i in range(N):
        for j in range(N):
            if board[i][j] != '*' and board[i][j] > res:
                res = board[i][j]
    
    return res



###################
# HELPER FUNCTION #
###################

def find_first_non_empty_cell(board, row, col, direction='RIGHT'):
    """
    Find the first non empty cell on the board based on the current positoin
    Only find in two directions: RIGHT and DOWN
    if find, return position, else, return None
    """
    N = len(board)

    if direction.upper() == 'RIGHT':
        # find in the same row:
        for k in range(col, N):
            if board[row][k] != '*':
                return row, k
        
    elif direction.upper() == 'DOWN':
        # find in the same col
        for k in range(row, N):
            if board[k][col] != '*':
                return k, col

    return None