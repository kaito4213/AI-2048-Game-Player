# Run in backend to test performance for different algorithms
# we measure a board using maximum score, and total score, and lasting moves

from algorithms.MCTS import naive_random_move
from algorithms.expectimax import expectimax
from algorithms.minimax import Minimax

from core.utils import *
from core.logic import *
import copy

# sample results output
# 'monte_carlo_simulation'
# simulates XX steps for each move
# {'max_tile':occur_times}
# {max scores}
# {'total_score': occur_times}
# average_moves to end of game


def get_results_mcts(which_algorithm = 'mcts', test_times = 5, sim_moves = (50,100,200,400,800)):

    res_all = []
    res_single = []

    total_score = {}

    max_total_scores = {}
    for sim_move in sim_moves:

        max_tiles = {}
        max_total_score = 0
        average_moves = 0
        for i in range(test_times):
            board = make_board(4)
            initial_two(board)
            curr_score = 0
            number_of_moves = 0
            board_info = {}

            while not check_end(board):
                action, successBoards = naive_random_move(board, curr_score, test_moves=sim_move)
                if can_move(board, action):
                    number_of_moves += 1

                    move(board, action)
                    curr_score += add_up_v2(board, action)
                    move(board, action)
                    simple_add_num(board)

            max_tile = find_max_cell(board)
            tile_counts = tile_count(board)

            board_info['movements'] = number_of_moves
            board_info['score'] = curr_score
            board_info['max_tile'] = max_tile
            board_info['depth'] = sim_move
            board_info['tile_count'] = tile_counts
            res_single.append(board_info)

            if max_tile not in max_tiles:
                max_tiles[max_tile] = 1
            else:
                max_tiles[max_tile] += 1
            if curr_score not in total_score:
                total_score[curr_score] = 1
            else:
                total_score[curr_score] += 1

            if max_total_score < curr_score:
                max_total_score = curr_score

            average_moves += number_of_moves

            # debug output
            print("Finish {} iteration when number of test simulation is {}".format(i, sim_move))

        max_total_scores[sim_move] = max_total_score

        res_all.append(which_algorithm + ' with sim_move {}'.format(sim_move))
        res_all.append(max_tiles)
        # res_all.append(total_score)
        # res_all.append(max_total_scores)
        res_all.append('Max_score is {}'.format(max_total_score))
        res_all.append('average_moves_till_end: {}'.format(average_moves/test_times))
        res_all.append('\n')

    res_all.append(max_total_scores)
    with open('results_{}_{}_{}.txt'.format(which_algorithm, 'total_count', str(sim_moves)), mode='wt', encoding='utf-8') as out:
        for e in res_all:
            out.write(str(e))
            out.write('\n')

    with open('results_{}_{}_{}.txt'.format(which_algorithm, 'single_count', str(sim_moves)), mode='wt', encoding='utf-8') as out:
        for e in res_single:
            out.write(str(e))
            out.write('\n')

    return res_all, res_single

def get_results_expectimax(which_algorithm = 'expectimax', test_times = 20, max_depth=(1,2)):
    moves = ('UP', 'DOWN', 'LEFT', 'RIGHT')

    res_all = []
    res_single = []

    total_score = {}


    for depth in max_depth:

        max_total_score = 0
        max_tiles = {}
        average_moves = 0
        for i in range(test_times):
            board = make_board(4)
            initial_two(board)
            curr_score = 0
            number_of_moves = 0
            board_info = {}

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
            tile_counts = tile_count(board)

            board_info['movements'] = number_of_moves
            board_info['score'] = curr_score
            board_info['max_tile'] = max_tile
            board_info['depth'] = depth
            board_info['tile_count'] = tile_counts
            res_single.append(board_info)

            if max_tile not in max_tiles:
                max_tiles[max_tile] = 1
            else:
                max_tiles[max_tile] += 1
            if curr_score not in total_score:
                total_score[curr_score] = 1
            else:
                total_score[curr_score] += 1
            if max_total_score < curr_score:
                max_total_score = curr_score
            average_moves += number_of_moves

            # debug output
            print("Finish {} iteration in depth {}".format(i, depth))

        res_all.append(which_algorithm + ' with depth {}'.format(depth))
        res_all.append(max_tiles)
        res_all.append('max score for this depth is {}'.format(max_total_score))
    # res_all.append(total_score)
        res_all.append('average_moves_till_end: {}'.format(average_moves/test_times))
        res_all.append('\n')

    with open('results_{}_{}_{}.txt'.format(which_algorithm, 'total_count', str(max_depth)), mode='wt', encoding='utf-8') as out:
        for e in res_all:
            out.write(str(e))
            out.write('\n')

    with open('results_{}_{}_{}.txt'.format(which_algorithm, 'single_count', str(max_depth)), mode='wt', encoding='utf-8') as out:
        for e in res_single:
            out.write(str(e))
            out.write('\n')

    return res_all, res_single

def get_results_minimax(which_algorithm='minimax', test_times=20, max_depth = (1,2,3,4)):

    res_all = []
    res_single = []

    total_score = {}


    for depth in max_depth:

        max_tiles = {}
        average_moves = 0
        max_total_score = 0

        for i in range(test_times):
            board = make_board(4)
            initial_two(board)
            curr_score = 0
            number_of_moves = 0
            board_info = {}

            player = Minimax(board, depth)

            while not check_end(board):
                best_move = player.basic_move()
                if can_move(board, best_move):
                    number_of_moves += 1
                    move(board,best_move)
                    curr_score += add_up_v2(board,best_move)
                    move(board,best_move)
                    simple_add_num(board)

            max_tile = find_max_cell(board)
            tile_counts = tile_count(board)

            board_info['movements'] = number_of_moves
            board_info['score'] = curr_score
            board_info['max_tile'] = max_tile
            board_info['depth'] = depth
            board_info['tile_count'] = tile_counts
            res_single.append(board_info)

            if max_tile not in max_tiles:
                max_tiles[max_tile] = 1
            else:
                max_tiles[max_tile] += 1
            if curr_score not in total_score:
                total_score[curr_score] = 1
            else:
                total_score[curr_score] += 1
            if max_total_score < curr_score:
                max_total_score = curr_score
            average_moves += number_of_moves

            # debug output
            print("Finish {} iteration in depth {}".format(i, depth))

        res_all.append(which_algorithm + ' with depth {}'.format(depth))
        res_all.append(max_tiles)
        res_all.append('max score for this depth is {}'.format(max_total_score))
        res_all.append('average_moves_till_end: {}'.format(average_moves / test_times))
        res_all.append('\n')

    with open('results_{}_{}_{}.txt'.format(which_algorithm, 'total_count', str(max_depth)), mode='wt', encoding='utf-8') as out:
        for e in res_all:
            out.write(str(e))
            out.write('\n')

    with open('results_{}_{}_{}.txt'.format(which_algorithm, 'single_count', str(max_depth)), mode='wt', encoding='utf-8') as out:
        for e in res_single:
            out.write(str(e))
            out.write('\n')

    return res_all, res_single



# get_results_expectimax()


## For each element, we generate a dictionary.
#{"movements: 1111,
#  "score": 111,
# "max_tile": 2048,
    # "depth": 2}

get_results_expectimax(max_depth=(1,2),test_times=5)