from utils import *
from logic import *

from sys import platform



ACTIONS = {'w': 'UP', 'W': 'UP', 's': 'DOWN', 'S': 'DOWN',
           'a': 'LEFT', 'A': 'LEFT', 'd': 'RIGHT', 'D': 'RIGHT'}


def win32_press():
    import keyboard
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


