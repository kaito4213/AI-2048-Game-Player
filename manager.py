from sys import platform
from core.gui import GameGrid
from core.logic import *
from core.utils import Actions
import copy
from algorithms.expectimax import expectimax


ACTIONS_MAP = {'w': 'UP', 'W': 'UP', 's': 'DOWN', 'S': 'DOWN',
           'a': 'LEFT', 'A': 'LEFT', 'd': 'RIGHT', 'D': 'RIGHT'}


def win32_press():
    import keyboard
    flag = True
    p = None
    while flag:
        try:
            for i in ACTIONS_MAP:
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
    while p not in ACTIONS_MAP:
        print("key press not recognized, please press wasd or WASD")
        p = key_press()
    return p


def run_console():
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
        action = ACTIONS_MAP[p]
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


def run_gui(algo):
    GameGrid(AI_mode=True, which_AI=algo)


def run(mode = "gui", algo = "expectimax"):
    if mode == "gui":
        run_gui(algo = algo)
    elif mode == "console":
        run_console()
    elif mode == "score":
        # This part is put here just for test visualizer.
        # Should be encapsulated in the future.
        if algo == "expectimax":
            board = make_board(4)
            initial_two(board)
            curr_score = 0
            while not check_end(board):
                depth = 2
                best_move = None
                best_val = -1

                for direction in Actions:
                    if not can_move(board, direction):
                        # clear()
                        continue

                    temp_board = copy.deepcopy(board)
                    move(temp_board, direction)
                    add_up(temp_board, direction, 0)
                    move(temp_board, direction)

                    alpha = expectimax(temp_board, depth)
                    if best_val < alpha:
                        best_val = alpha
                        best_move = direction

                move(board,best_move)
                curr_score += add_up_v2(board, best_move)
                move(board,best_move)
                simple_add_num(board)
            max_cell = find_max_cell(board)
            return curr_score, max_cell
        else:
            raise ValueError("No such algorithm: {}".format(algo))

    else:
        raise ValueError("Unexpect Mode. Choose one from 'gui' or 'console'")

if __name__ == "__main__":
    run(mode = "gui", algo = "expectimax")


