import copy
import numpy as np

from core.logic import *
from core.utils import *

moves = ('UP', 'DOWN', 'LEFT', 'RIGHT')
prob = {0: 0, 2: 0.9, 4: 0.1}


def eval_score(board):
    """
    evaluate the score for current score
    """
    N = len(board)
    eval_matrix = [[1 for i in range(N)] for i in range(N)]
    eval_matrix = np.array(eval_matrix)

    eval_matrix[0][0] = 2 ** 15
    eval_matrix[0][1] = 2 ** 14
    eval_matrix[0][2] = 2 ** 13
    eval_matrix[0][3] = 2 ** 12

    eval_matrix[1][0] = 2 ** 8
    eval_matrix[1][1] = 2 ** 9
    eval_matrix[1][2] = 2 ** 10
    eval_matrix[1][3] = 2 ** 11

    eval_matrix[2][0] = 2 ** 7
    eval_matrix[2][1] = 2 ** 6
    eval_matrix[2][2] = 2 ** 5
    eval_matrix[2][3] = 2 ** 4

    eval_matrix[3][0] = 2 ** 0
    eval_matrix[3][1] = 2 ** 1
    eval_matrix[3][2] = 2 ** 2
    eval_matrix[3][3] = 2 ** 3

    # print(eval_matrix)

    score = 0
    for i in range(N):
        for j in range(N):
            if board[i][j] != '*':
                score += board[i][j] * eval_matrix[i][j]

    return score


def expectimax(board, depth):
    tot_score = 0
    tot_prob = 0
    if depth == 0:
        return eval_score(board)

    else:
        for empty in find_empty_cells(board):
            best_score = 0
            best_move = None

            #generate new number in board
            new_board = copy.deepcopy(board)
            row, col = empty
            p = random.randint(0, 99)
            #new_num = 0
            if p < 90:
                new_num = 2
            else:
                new_num = 4

            new_board[row][col] = new_num

            for directions in moves:
                if not can_move(board, directions):
                    continue

                #move new board in dir
                temp_board = copy.deepcopy(new_board)
                move(temp_board, directions)
                add_up(temp_board, directions, 0)
                move(temp_board, directions)
                score = expectimax(temp_board, depth - 1)

                if score > best_score:
                    best_score = score
                    best_move = directions

            if best_move != None:
                tot_score += prob[new_num] * best_score
            else:
                tot_score += prob[new_num] * eval_score(temp_board)
            tot_prob += prob[new_num]

        if tot_prob == 0:
            return tot_score

        return tot_score / tot_prob


def run_expectimax():
    board = make_board(4)
    initial_two(board)
    print_board(board)

    total_moves = 0
    depth = 1

    while not check_end(board):
        best_move = None
        best_val = -1

        for direction in moves:
            if not can_move(board, direction):
                #clear()
                continue

            temp_board = copy.deepcopy(board)
            move(temp_board, direction)
            add_up(temp_board, direction, 0)
            move(temp_board, direction)

            alpha = expectimax(temp_board, depth)
            if best_val < alpha:
                best_val = alpha
                best_move = direction

        move(board, best_move)
        add_up(board, best_move, 0)
        move(board, best_move)
        total_moves += 1
        clear()
        print_board(board)
        simple_add_num(board)


if __name__ == "__main__":
    run_expectimax()


