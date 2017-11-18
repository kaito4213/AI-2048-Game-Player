from logic import *
from utils import *
from Game_Manager import initial_two, place_two


import numpy as np
import time
import random
import copy

keyboard_action = {'w': 'UP', 'W': 'UP', 's': 'DOWN', 'S': 'DOWN',
                   'a': 'LEFT', 'A': 'LEFT', 'd': 'RIGHT', 'D': 'RIGHT'}

def naive_random_move(board, curr_score, test_moves=100):
    """
    based on current board, and current score, return the next move
    four moves, randomly choose, and then take random moves until hit test_moves times or no longer survive
    compare scores of each direction, choose the largest one

    return value is one of action
    """

    moves = ('UP', 'DOWN', 'LEFT', 'RIGHT')

    successBoards = []

    scores = [curr_score for i in range(len(moves))]
    for i in range(len(moves)):
        action = moves[i]
        test_board = copy.deepcopy(board)

        if can_move(test_board, action):

            move(test_board, action)
            scores[i] = add_up(test_board, action, scores[i])
            move(test_board, action)
            simple_add_num(test_board)

            test_times = test_moves - 1
            run_times = 0
            # while test_times > 0 and not check_end(test_board):
            while not check_end(test_board):
                test_action = moves[random.randint(0, 3)]
                # print("test for action", test_action, " in the ", test_times, " test times")
                # print_board(test_board)
                if can_move(test_board, test_action):

                    move(test_board, test_action)
                    scores[i] = add_up(test_board, test_action, scores[i])
                    move(test_board, test_action)
                    simple_add_num(test_board)
                    run_times += 1
                    test_times -= 1

            if find_max_cell(test_board) > 4096:
                successBoards.append(test_board)

    if max(scores) == curr_score:
        print("this time the AI can not make a move")
        return moves[random.randint(0, 3)], successBoards
    else:
        return moves[scores.index(max(scores))], successBoards


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

    row, col = emptyCells[random.randint(0, len(emptyCells) - 1)]
    random.seed()
    p = random.randint(0, 99)
    if p < 90:
        board[row][col] = 2
    else:
        board[row][col] = 4


def MCTS_place_two(board):
    """
    place two number in the board

    first find all the empy cells
    if has > 2 empty cells, 95% add two number, 5% add one number
    if has < 2 empty cells, 95% add one number, 5% add no number

    if add two number:
        one must be 2,
        another 90% 2

    if add onw number:
        90% 2
    """
    N = len(board)
    emptyCells = find_empty_cells(board)

    num_emptyCell = len(emptyCells)
    if num_emptyCell == 0:
        print("no empty cells")
        return

    add_how_many_number = 0
    if num_emptyCell > 2:
        p = random.randint(0, 99)
        if p < 95:
            add_how_many_number = 2
        else:
            add_how_many_number = 1
    else:
        p = random.randint(0, 99)
        if p < 95:
            add_how_many_number = 1
        else:
            add_how_many_number = 0

    if add_how_many_number == 0:
        print("Not add one number, move on")
        return
    elif add_how_many_number == 1:
        # 80% add 2, 20% add 1
        x1, y1 = emptyCells[random.randint(0, num_emptyCell - 1)]
        p = random.randint(0, 99)
        if p < 90:
            board[x1][y1] = 2
        else:
            board[x1][y1] = 4
    elif add_how_many_number == 2:
        x1, y1 = emptyCells[random.randint(0, num_emptyCell - 1)]
        x2, y2 = emptyCells[random.randint(0, num_emptyCell - 1)]
        while (x2, y2) == (x1, y1):
            x2, y2 = emptyCells[random.randint(0, num_emptyCell - 1)]

        # first number be 2
        board[x1][y1] = 2

        # for second added number
        # 80% add 2, 20% add 4
        p = random.randint(0, 99)
        if p < 60:
            board[x2][y2] = 2
        else:
            board[x2][y2] = 4


def run_naive_MCTS(N=4,test_moves=100):

    random.seed()

    board = make_board(N)
    initial_two(board)
    print_board(board)
    curr_score = 0

    stuck = 0
    human = False
    while not check_end(board):

        print(" ")
        print("current score is, ", curr_score)
        print("Possible actions: up, left, right, down, exit")
        if not human:
            action, successBoards = naive_random_move(
                board, curr_score, test_moves)
            if len(successBoards) > 0:
                c = input("find success board in test run, please press enter")
                for successBoard in successBoards:
                    print_board(successBoard)
                    print(" ")
                c = input("press enter to continue...")
            action = action.upper()
        else:
            print("AI stuck, need human help ")
            print("Possible actions: up, left, right, down, exit")
            action = input('Your action: ')
            action = action.upper()
            human = False

        if action == "EXIT":
            break
        # take action here to do the move
        # and clear current , then print board
        if can_move(board, action):
            move(board, action)
            curr_score = add_up(board, action, curr_score)
            move(board, action)
            clear()
            simple_add_num(board)
            print_board(board)
            print(" ")
        else:
            stuck += 1
            # clear()
            # print_board(board)
            print("action is ", action, " but can not move")
            if stuck >= 10:
                clear()
                print_board(board)
                stuck = 0
                human = True

        # time.sleep(0.2)
    print("Your Score is ", curr_score)
    print("Max number in board is", find_max_cell(board))
    print("Game end")
    return find_max_cell(board)


def human_run():
    board = make_board(4)
    initial_two(board)
    print_board(board)
    curr_score = 0
    while not check_end(board):
        print(" ")
        print("current score is, ", curr_score)
        print("Possible actions: up, left, right, down, exit")
        print("Please press WASD for UP LEFT DOWN RIGHT")
        action = keyboard_action[keyPress()]
        action = action.upper()
        if action == "EXIT":
            break
        # take action here to do the move
        # and clear current , then print board
        if can_move(board, action):
            move(board, action)
            curr_score = add_up(board, action, curr_score)
            move(board, action)
            clear()
            simple_add_num(board)
            print_board(board)
        else:
            clear()
            print_board(board)
    print("")
    print("Game end")
    print("Your Score is ", curr_score)
    print("Max number in board is", find_max_cell(board))
    print("To run this game, type run()")


def run_many_times():
    how_many_times = 50
    max_score = 0
    scores = {}
    while how_many_times >= 0:
        max_score = run_naive_MCTS(test_moves=100)
        if max_score in scores:
            scores[max_score] += 1
        else:
            scores[max_score] = 1
        how_many_times -= 1

    print(scores)


def evalScore(board):
    """
    evaluate the score for current score
    """
    N = len(board)
    eval_matrix = [[1 for i in range(N)] for i in range(N)]
    eval_matrix = np.array(eval_matrix)
    
    eval_matrix[0][0] = 4 ** 15
    eval_matrix[0][1] = 4 ** 14
    eval_matrix[0][2] = 4 ** 13
    eval_matrix[0][3] = 4 ** 12

    eval_matrix[1][0] = 4 ** 8
    eval_matrix[1][1] = 4 ** 9
    eval_matrix[1][2] = 4 ** 10
    eval_matrix[1][3] = 4 ** 11
    
    eval_matrix[2][0] = 4 ** 7
    eval_matrix[2][1] = 4 ** 6
    eval_matrix[2][2] = 4 ** 5
    eval_matrix[2][3] = 4 ** 4

    eval_matrix[3][0] = 4 ** 0
    eval_matrix[3][1] = 4 ** 1
    eval_matrix[3][2] = 4 ** 2
    eval_matrix[3][3] = 4 ** 3
    
    # print(eval_matrix)

    score = 0
    for i in range(N):
        for j in range(N):
            if board[i][j] != '*':
                score += board[i][j] * eval_matrix[i][j]

    return score