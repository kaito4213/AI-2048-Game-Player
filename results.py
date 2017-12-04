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


def get_results_mcts(which_algorithm = 'mcts', test_times = 5):
    res = []

    total_score = {}
    sim_moves = (50,100,200,400,800)
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

            while not check_end(board):
                action, successBoards = naive_random_move(board, curr_score, test_moves=sim_move)
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

            if max_total_score < curr_score:
                max_total_score = curr_score

            average_moves += number_of_moves

            # debug output
            print("Finish {} iteration when number of test simulation is {}".format(i, sim_move))

        max_total_scores[sim_move] = max_total_score

        res.append(which_algorithm + ' with sim_move {}'.format(sim_move))
        res.append(max_tiles)
        # res.append(total_score)
        # res.append(max_total_scores)
        res.append('Max_score is {}'.format(max_total_score))
        res.append('average_moves_till_end: {}'.format(average_moves/test_times))
        res.append('\n')

    res.append(max_total_scores)
    with open('results_{}.txt'.format(which_algorithm), mode='wt', encoding='utf-8') as out:
        for e in res:
            out.write(str(e))
            out.write('\n')

    return res

def get_results_expectimax(which_algorithm = 'expectimax', test_times = 20):
    moves = ('UP', 'DOWN', 'LEFT', 'RIGHT')

    res = []

    total_score = {}


    for depth in (1,2):

        max_total_score = 0
        max_tiles = {}
        average_moves = 0
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
            if max_total_score < curr_score:
                max_total_score = curr_score
            average_moves += number_of_moves

            # debug output
            print("Finish {} iteration in depth {}".format(i, depth))

        res.append(which_algorithm + ' with depth {}'.format(depth))
        res.append(max_tiles)
        res.append('max score for this depth is {}'.format(max_total_score))
    # res.append(total_score)
        res.append('average_moves_till_end: {}'.format(average_moves/test_times))
        res.append('\n')

    with open('results_{}.txt'.format(which_algorithm), mode='wt', encoding='utf-8') as out:
        for e in res:
            out.write(str(e))
            out.write('\n')

    return res

def get_results_minimax(which_algorithm='minimax', test_times=2):

    res = []
    total_score = {}

    max_depths = (2,3,4,5,6,7,8,9,10,11,12,13,14)

    for depth in max_depths:

        max_tiles = {}
        average_moves = 0
        max_total_score = 0

        for i in range(test_times):
            board = make_board(4)
            initial_two(board)
            curr_score = 0
            number_of_moves = 0

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

        res.append(which_algorithm + ' with depth {}'.format(depth))
        res.append(max_tiles)
        res.append('max score for this depth is {}'.format(max_total_score))
        res.append('average_moves_till_end: {}'.format(average_moves / test_times))
        res.append('\n')

    with open('results_{}.txt'.format(which_algorithm), mode='wt', encoding='utf-8') as out:
        for e in res:
            out.write(str(e))
            out.write('\n')

    return res



# get_results_expectimax()


## For each element, we generate a dictionary.
#{"movements: 1111,
#  "score": 111,
# "max_tile": 2048,
    # "depth": 2}