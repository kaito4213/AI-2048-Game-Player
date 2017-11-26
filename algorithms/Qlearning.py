import copy
import numpy as np
from core.evaluate_function import *
from core.logic import *
from core.utils import *

def initialization():
    """
    decrease_pairs represents the number of pairs in which the second number is
    less than the first number, empty number is taken as 0
    in 2048 game, the board is snake-shaped
    128(1) 32(2) *(3)  *(4)
    16(8)  62(7) 2(6)  4(5)
    *(9)   *(10) *(11) 2(12)
    *(16)  *(15) 2(14) *(13)
    so the monotonicity of this board is 7

    each state in game 2048 can be defined as (decrease_pairs, empty_cells, max_merge)
    there are 16*16*9=2304 states in total
    """
    decrease_pairs = np.arange(16)
    empty_cells = np.arange(16)
    max_merge = np.arange(9)

    states = []
    for i in decrease_pairs:
        for j in empty_cells:
            for k in max_merge:
                states.append((i, j, k))

    # initial Q value for each state
    values = {}
    for state in states:
        values[state] = 0

    return values

def reward(state1, state2):
    """
        immediate reward for each state
        earn 10 for any new empty cell
        earn 10 for any merge
        earn 50 for increament of decreasing pairs
    """
    empty_cell = 10
    merge_cell = 30
    increase_pair = 100

    score = increase_pair*(state2[0] - state1[0]) \
            + empty_cell*(state2[1] - state1[1])\
            + merge_cell*(state2[2] - state1[2])

    return score

def get_Q(actions, Q, state1, state2):
    """
       values will contain the discounted sum of the rewards to be earned (on average)
    """
    if len(actions) == 0:
        return 0

    p = 1/len(actions)
    gamma = 0.9
    Q_value = p * (reward(state1, state2) + gamma * Q[state2])
    return Q_value

def update_Q_value(actions, Q, state1, state2):
    Q[state1] = get_Q(actions, Q, state1, state2)

def get_state(board):
    state_list = []
    evaluation = Evaluator(board)
    state_list.append(evaluation.decreasement())
    state_list.append(evaluation.emptiness(board))
    state_list.append(evaluation.maximum_merge_cells())
    state = tuple(state_list)

    return state

moves = ('UP', 'DOWN', 'LEFT', 'RIGHT')
def training(Q):
    #initialize game
    board = make_board(4)
    initial_two(board)

    while not check_end(board):
        actions = []
        next_move = None
        max_Q =  float('-inf')
        old_state = get_state(board)

        #get all valid actions for current state
        for direction in moves:
            if can_move(board, direction):
                actions.append(direction)
        #find the policy that maximize Q
        for direction in actions:
            tmp_board = copy.deepcopy(board)
            move(tmp_board, direction)
            add_up(tmp_board, direction, 0)
            move(tmp_board, direction)
            new_state = get_state(board)
            Q_value = get_Q(actions, Q, old_state, new_state)
            if Q_value >= max_Q:
                max_Q = Q_value
                next_move = direction

        #update Q value
        #print('before',board)
        move(board, next_move)
        add_up(board, next_move, 0)
        move(board, next_move)
        #print('after', board)
        new_state = get_state(board)
        update_Q_value(actions, Q, old_state, new_state)
        simple_add_num(board)

    print(find_max_cell(board))

def run_Qlearning():
    Q = initialization()
    iteration = 10000

    while(iteration > 0):
        training(Q)
        iteration -= 1

    print(Q)
    #test by using current Q
    training(Q)

if __name__ == "__main__":
    run_Qlearning()
