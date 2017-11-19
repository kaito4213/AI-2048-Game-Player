from utils import *
from logic import *
import random
from sys import platform
import keyboard


ACTIONS = {'w': 'UP', 'W': 'UP', 's': 'DOWN', 'S': 'DOWN',
           'a': 'LEFT', 'A': 'LEFT', 'd': 'RIGHT', 'D': 'RIGHT'}

class Board():

    def __init__(self, size = 4):
        """
        Init a game board, default dimension is 4
        """
        self.N = 4
        self.board = make_board(self.N)


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
    place two number in the boar
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


def win32_press():
    flag = True
    p = None
    while flag:
        try:
            for i in ACTIONS:
                if keyboard.is_pressed(i):
                    p = i
                    flag = False
                    break
            for i in ["q", "Q"]:
                if keyboard.is_pressed(i):
                    p = i
                    flag = False
                    break
        except:
            pass
    return p

def linux_press():
    p = key_press()
    while p not in ACTIONS:
        print("key press not recognized, please press wasd or WASD")
        p = key_press()
    return p

def run():
    board = make_board(4)
    initial_two(board)
    print_board(board)
    curr_score = 0
    while not check_end(board):
        print("\ncurrent score is, ", curr_score)
        print("Possible actions: up, left, right, down, exit")
        print("Please press WASD for UP LEFT DOWN RIGHT Q for exit")

        if platform.startswith('linux') or platform == 'darwin':
            p = linux_press()
        elif platform == 'win32' or platform == 'cygwin':
            p = win32_press()
        else:
            p = win32_press()

        if p == 'q' or p == 'Q':
            break
        action = ACTIONS[p]
        action = action.upper()
        if action == "EXIT":
            break
        # take action here to do the move
        # and clear current , then print board
        if can_move(board, action):
            move(board, action)
            curr_score = add_up(board, action, curr_score)
            # move(board, action)
            clear()
            simple_add_num(board)
            print_board(board)
        else:
            clear()
            print_board(board)
    print("/nGame end/nTo run this game, type run_keyboard()")



if __name__ == "__main__":
    run()

