import random

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
    return a list of empty cells. Use tupe to represent the coordinates in the matrix.
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


def key_press():
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


def initial_two(board):
    """
    initial two on the board
    place_two() only uses after each move, because place two some times place no number
    which should not occur in the beginning
    """
    N = len(board)
    x1, y1 = random.randint(0,N-1), random.randint(0,N-1)
    times = 0
    while times < 10 and board[x1][y1] != '*':
        x1, y1 = random.randint(0,N-1), random.randint(0,N-1)
        times += 1

    if board[x1][y1] == '*':
        board[x1][y1] = 2

    times = 0
    x1, y1 = random.randint(0,N-1), random.randint(0,N-1)
    while times < 3 and board[x1][y1] != '*':
        x1, y1 = random.randint(0,N-1), random.randint(0,N-1)
        times += 1

    if board[x1][y1] == '*':
        board[x1][y1] = 4


def place_two(board):
    """
    place two number in the board
    """
    N = len(board)
    random_generate_2 = random.randint(0,10)
    # generate a new number of 2 with possibily of 50%
    if random_generate_2 < 5:
        x1, y1 = random.randint(0,N-1), random.randint(0,N-1)
        times = 0
        while times < 10 and board[x1][y1] != '*':
            x1, y1 = random.randint(0,N-1), random.randint(0,N-1)
            times += 1

        if board[x1][y1] == '*':
            board[x1][y1] = 2

    random_generate_4 = random.randint(0, 10)
    # generate a new number of 2 with possibily of 30%
    if random_generate_4 < 3:
        times = 0
        x1, y1 = random.randint(0,N-1), random.randint(0,N-1)
        while times < 3 and board[x1][y1] != '*':
            x1, y1 = random.randint(0,N-1), random.randint(0,N-1)
            times += 1

        if board[x1][y1] == '*':
            board[x1][y1] = 4


def simple_add_num(board):
    """
    simple add a number in the board

    if tile has empty, find it, and then
    90% add 2
    10% add 4

    """
    emptyCells = find_empty_cells(board)
    if len(emptyCells) == 0:
        print("no empty cells, return")
        return

    row, col = emptyCells[random.randint(0, len(emptyCells)-1)]
    p = random.randint(0,99)
    if p < 90:
        board[row][col] = 2
    else:
        board[row][col] = 4