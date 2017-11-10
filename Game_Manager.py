from utils import *
from logic import *
import random

class Board():

    def __init__(self, size = 4):
        """
        Init a game board, default dimension is 4
        """
        self.N = 4
        self.board = make_board(self.N)


def place_two(board):
    """
    place two number in the board
    """
    N = len(board)
    x1, y1 = random.randint(0,N-1), random.randint(0,N-1)
    times = 0
    while times < 10 and board[x1][y1] != '*':
        x1, y1 = random.randint(0,N-1), random.randint(0,N-1)
        times += 1
    board[x1][y1] = 2

    times = 0
    x1, y1 = random.randint(0,N-1), random.randint(0,N-1)
    while times < 3 and board[x1][y1] != '*':
        x1, y1 = random.randint(0,N-1), random.randint(0,N-1)
        times += 1
    board[x1][y1] = 4

def run():
    board = make_board(4)
    place_two(board)
    print_board(board)
    while not check_end(board):
        print(" ")
        print("Possible actions: up, left, right, down, exit")
        action = input('Your action: ')
        action = action.upper()
        if action == "EXIT":
            break
        # take action here to do the move
        # and clear current , then print board
        if can_move(board, action):
            move(board, action)
            add_up(board, action)
            move(board, action)
            clear()
            place_two(board)
            print_board(board)
        else:
            clear()
            print_board(board)
    print("Game end")
    print("To run this game, type run()")

if __name__ == "__main__":
    run()