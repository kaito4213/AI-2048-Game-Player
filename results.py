# Run in backend to test performance for different algorithms
# we measure a board using maximum score, and total score, and lasting moves

from algorithms.MCTS import naive_random_move
from algorithms.expectimax import expectimax
from core.utils import *
from core.logic import *
import copy

# sample results output
# 'monte_carlo_simulation'
# simulates XX steps for each move
# {'max_tile':occur_times}
# {'total_score': occur_times}
# average_moves to end of game


def get_results_mcts(which_algorithm = 'mcts', test_times = 20):
    res = []
    max_tiles = {}
    total_score = {}
    average_moves = 0
    for i in range(test_times):
        board = make_board(4)
        initial_two(board)
        curr_score = 0
        number_of_moves = 0
        while not check_end(board):
            while not check_end(board):
                action, successBoards = naive_random_move(board, curr_score, test_moves=1)
                if can_move(board, action):
                    number_of_moves += 1

                    move(board, action)
                    curr_score += add_up_v2(board, action)
                    move(board, action)
                    simple_add_num(board)

            max_tile = find_max_cell(board)

            if max_tile not in max_tiles:
                max_tiles[max_tile] = 1
            else:
                max_tiles[max_tile] += 1
            if curr_score not in total_score:
                total_score[curr_score] = 1
            else:
                total_score[curr_score] += 1
        average_moves += number_of_moves

    res.append(which_algorithm)
    res.append(max_tiles)
    # res.append(total_score)
    res.append('average_moves_till_end: {}'.format(average_moves/test_times))

    with open('results_{}.txt'.format(which_algorithm), mode='wt', encoding='utf-8') as out:
        for e in res:
            out.write(str(e))
            out.write('\n')

    return res

def get_results_expectimax(which_algorithm = 'expectimax', test_times = 3):
    moves = ('UP', 'DOWN', 'LEFT', 'RIGHT')

    res = []
    max_tiles = {}
    total_score = {}
    average_moves = 0

    for depth in (1,2):
        for i in range(test_times):
            board = make_board(4)
            initial_two(board)
            curr_score = 0
            number_of_moves = 0

            # depth = 1

            while not check_end(board):
                best_move = None
                best_val = -1

                for direction in moves:
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

                number_of_moves += 1
                move(board, best_move)
                curr_score += add_up_v2(board, best_move)
                move(board, best_move)
                simple_add_num(board)

            max_tile = find_max_cell(board)

            if max_tile not in max_tiles:
                max_tiles[max_tile] = 1
            else:
                max_tiles[max_tile] += 1
            if curr_score not in total_score:
                total_score[curr_score] = 1
            else:
                total_score[curr_score] += 1
            average_moves += number_of_moves

        res.append(which_algorithm + str(depth))
        res.append(max_tiles)
    # res.append(total_score)
        res.append('average_moves_till_end: {}'.format(average_moves/test_times))

    with open('results_{}.txt'.format(which_algorithm), mode='wt', encoding='utf-8') as out:
        for e in res:
            out.write(str(e))
            out.write('\n')

    return res


get_results_expectimax()