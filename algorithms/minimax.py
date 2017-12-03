# ACKNOWLEDGEMENT:
# The idea of implementation comes from the following courses, codes and answers:
# https://www.youtube.com/watch?v=STjW3eH0Cik&t=2128s
# https://github.com/ss4936/2048
# https://github.com/ovolve/2048-AI/tree/master/js
# https://stackoverflow.com/questions/22342854/what-is-the-optimal-algorithm-for-the-game-2048/22389702#22389702

from core.evaluate_function import MinimaxEvaluator
import numpy as np
import copy as cp
import math
from core.logic import can_move, check_end, move, add_up_v2
from core.utils import Actions, find_empty_cells

class Minimax:
    def __init__(self, board = None, max_depth = 4):
        self.board = board
        self.max_depth = max_depth
        self.ACTIONS = Actions

    def eval(self, board):
        '''
        A evaluation function
        '''
        me = MinimaxEvaluator(board)
        empty_counts = me.emptiness()
        smooth_weight = 0.1
        mono_weight = 1.0
        empty_weight = 2.7
        max_weight = 1.0
        smooth = me.smoothness()*smooth_weight
        mono = me.monotonicity() * mono_weight
        # When no empty cells the while loop should terminate.
        # So no need to consider it here.
        if(empty_counts == 0):
            emp = -np.inf
        else:
            emp = math.log(empty_counts, 2) * empty_weight
        maxwgt = me.max_val() * max_weight
        return smooth + mono + emp + maxwgt

    def basic_move(self):
        '''
        This function return direction calculate by a basic/ non-pruning algorithm
        :return: a direction string
        '''
        best_move = None
        max_value = -np.inf
        # currently is max player. Facing on 4 directions, you iterate, compare the heuristic,
        # choose the best direction to go.
        for action in self.ACTIONS:
            # best_value = -np.inf
            board_copy = cp.deepcopy(self.board)
            if can_move(board_copy, action):
                move(board_copy, action)
                add_up_v2(board_copy,action)
                move(board_copy, action)
                best_value = self.basic_run(board_copy, self.max_depth, False)
            # if action == "RIGHT" or action == "DOWN":
            #     best_value += 500
                if best_value > max_value:
                    max_value = best_value
                    best_move = action
        if best_move == None:
            # raise ValueError("The best move is None! Check minimax algorithm.")
            return self.ACTIONS[np.random.randint(0,3)]
        return best_move

    def basic_run(self, board, max_depth, is_max):
        if (max_depth == 0) or check_end(board):
            return self.eval(board)
        if is_max:
            best_value = -np.inf
            children = []
            for action in self.ACTIONS:
                board_copy = cp.deepcopy(board)
                if can_move(board_copy, action):
                    move(board_copy, action)
                    add_up_v2(board_copy, action)
                    move(board_copy, action)
                    children.append(board_copy)
            for child in children:
                best_value = max(best_value, self.basic_run(child, max_depth - 1, False))

            return best_value
        else:
            best_value = np.inf
            children = []
            empty_cells = find_empty_cells(board)
            for cell in empty_cells:
                board_copy = cp.deepcopy(board)
                board_copy[cell[0]][cell[1]] = 2
                children.append(board_copy)
                board_copy = cp.deepcopy(board)
                board_copy[cell[0]][cell[1]] = 4
                children.append(board_copy)
            for child in children:
                best_value = min(best_value, self.basic_run(child, max_depth - 1, True))
            return best_value




    def alpha_beta_move(self):
        '''
        This function return direction calculate by a alpha-beta pruning algorithm
        :return: a direction string
        '''
        best_move = None
        max_value = -np.inf
        # currently is max player. Facing on 4 directions, you iterate, compare the heuristic,
        # choose the best direction to go.
        for action in self.ACTIONS:
            best_value = -np.inf
            board_copy = cp.deepcopy(self.board)
            if can_move(board_copy, action):
                move(board_copy, action)
                add_up_v2(board_copy,action)
                move(board_copy,action)
                best_value = self.alpha_beta_run(board_copy, self.max_depth, -np.inf, np.inf, False)
            # if action == "RIGHT" or action == "DOWN":
            #     best_value += 500
            if best_value >= max_value:
                max_value = best_value
                best_move = action
            print(best_value)
        if best_move == None:
            raise ValueError("The best move is None! Check minimax algorithm.")
        return best_move

    def alpha_beta_run(self, board, max_depth, alpha, beta, is_max):
        if max_depth == 0:
            return self.eval(board)
        if not check_end(board):
            return self.eval(board)

        if is_max:
            best_value = -np.inf
            children = []
            for action in self.ACTIONS:
                board_copy = cp.deepcopy(board)
                if can_move(board_copy, action):
                    move(board_copy, action)
                    add_up_v2(board_copy, action)
                    move(board_copy, action)
                    children.append(board_copy)
            for child in children:
                best_value = max(best_value, self.alpha_beta_run(child, max_depth - 1, alpha, beta, False))
                if best_value >= beta:
                    return best_value
                alpha = max(alpha, best_value)
            return best_value
        else:
            best_value = np.inf
            children = []
            empty_cells = find_empty_cells(board)
            for cell in empty_cells:
                board_copy = cp.deepcopy(board)
                board_copy[cell[0]][cell[1]] = 2
                children.append(board_copy)
                board_copy = cp.deepcopy(board)
                board_copy[cell[0]][cell[1]] = 4
                children.append(board_copy)
            for child in children:
                best_value = min(best_value, self.alpha_beta_run(child, max_depth - 1, alpha, beta, True))
                if best_value <= alpha:
                    return best_value
                beta = min(beta, best_value)
            return best_value

