Actions = ("Up", "Down", "Left", "Right")

def make_board(N):
    assert N >= 1, "Invalid Dimension"
    assert type(N) == int, "N must be Integer"

    board = [['*' for i in range(N)] for i in range(N)]
    return board


def print_board(board):
    """
    print board what look like
    """
    N = len(board)
    for row in range(0,N):
        print("           ")
        for col in range(0,N):
            if board[row][col] != '*':
                print(repr(board[row][col]).ljust(5), end="")
            else:
                print(board[row][col].ljust(5), end="")

def check_full(board):
    """
    Check if board is full
    """
    N = len(board)
    for i in range(N):
        for j in range(N):
            if board[i][j] == '*':
                return False
    return True

def find_empty_cells(board):
    """
    find all empty cells
    """
    emptyCells = []
    N = len(board)
    for i in range(N):
        for j in range(N):
            if board[i][j] == '*':
                emptyCells.append((i,j))
    
    return emptyCells
    
def find_max_cell(board):
    """
    find the maximum number in the cell
    """
    N = len(board)
    best_cell = 0
    for i in range(N):
        for j in range(N):
            if board[i][j] != '*' and board[i][j] > best_cell:
                best_cell = board[i][j]
    
    return best_cell

def check_end(board):
    """
    check if game is at the end state
    """
    N = len(board)

    # first check if full, and if full, check no two adjacent elem is same
    if not check_full(board):
        return False
    
    # check row
    for i in range(N):
        for j in range(1,N):
            if board[i][j] == board[i][j-1]:
                return False
    
    # check col
    for i in range(N):
        for j in range(1,N):
            if board[j][i] == board[j-1][i]:
                return False
    
    return True

def get_elem(board, p):
    """
    get the elem in board position p(x, y)
    """
    x, y = p
    N = len(board)
    if x < 0 or x >= N or y < 0 or y >= N:
        return None

    return board[x][y]

def place_elem(board, p, elem):
    """
    place elem into the board position p(x, y)
    """
    x, y = p
    N = len(board)
    if x < 0 or x >= N or y < 0 or y >= N:
        return None
    board[x][y] = elem
    return True


def swap(board, p1, p2):
    """
    Swap two elem on board in postition p1, p2
    """
    x1, y1 = p1
    x2, y2 = p2
    board[x1][y1], board[x2][y2] = board[x2][y2], board[x1][y1]

def clear():
    """
    clear the console
    """
    import os
    b = os.system("clear")


def keyPress():
    """
    simulate a key press event, may not work on Windows
    tested in Ubuntu
    """
    import tty
    import sys
    import termios

    orig_settings = termios.tcgetattr(sys.stdin)
    tty.setraw(sys.stdin)

    x = 0

    if x != chr(27):
        x = sys.stdin.read(1)[0]
        # print("You pressed ", x)

    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, orig_settings)
    return x

def add_up_v2(board, action):
    """
    After each move, we need to add up the same elem
    """    
    add_score = 0
    N = len(board)
    if action == "UP":
        for col in range(0,N):
            for j in range(0, N-1):
                if board[j][col] == board[j+1][col] and board[j][col] != '*':
                    add_score += 2 * board[j][col]
                    board[j][col] = board[j][col] + board[j+1][col]
                    board[j+1][col] = '*'

    if action == "DOWN":
        for col in range(0,N):
            j = N-1
            while j > 0:
                if board[j][col] == board[j-1][col] and board[j][col] != '*':
                    add_score += 2 * board[j][col]
                    board[j][col] = board[j][col] + board[j-1][col]
                    board[j-1][col] = '*'
                j -= 1

    if action == "LEFT":
        for row in range(0, N):
            for j in range(0, N-1):
                if board[row][j] == board[row][j+1] and board[row][j] != '*':
                    add_score += 2 * board[row][j]
                    board[row][j] = board[row][j] + board[row][j+1]
                    board[row][j+1] = '*'

    if action == "RIGHT":
        for row in range(0,N):
            j = N-1
            while j > 0:
                if board[row][j] == board[row][j-1] and board[row][j] != '*':
                    add_score += 2 * board[row][j]
                    board[row][j] = board[row][j] + board[row][j-1]
                    board[row][j-1] = '*'
                j -= 1

    return add_score
