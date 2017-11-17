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

def run():
    board = make_board(4)
    # place_two(board)
    initial_two(board)
    print_board(board)
    curr_score = 0
    while not check_end(board):
        print(" ")
        print("current score is, ",curr_score)
        print("Possible actions: up, left, right, down, exit")
        action = input('Your action: ')
        action = action.upper()
        if action == "EXIT":
            break
        # take action here to do the move
        # and clear current , then print board
        if can_move(board, action):
            move(board, action)
            curr_score = add_up(board, action,curr_score)
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