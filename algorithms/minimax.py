# ACKNOWLEDGEMENT:
# The idea of implementation comes from the following courses, codes and answers:
# https://www.youtube.com/watch?v=STjW3eH0Cik&t=2128s
# https://github.com/ss4936/2048
# https://github.com/ovolve/2048-AI/tree/master/js
# https://stackoverflow.com/questions/22342854/what-is-the-optimal-algorithm-for-the-game-2048/22389702#22389702

from core.evaluate_function import MinimaxEvaluator
import numpy as np
from core.logic import can_move, check_end, move
from core.utils import Actions, find_empty_cells

class Minimax:
    def __init__(self, board = None, max_depth = 4, actions = Actions):
        self.board = board
        self.max_depth = max_depth
        self.ACTIONS = actions
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
        return me.smoothness() + me.monotonicity() + np.log(empty_counts) + me.max_val()

    def basic_move(self):
        '''
        This function return direction calculate by a basic/ non-pruning algorithm
        :return: a direction string
        '''
        best_move = None
        max_value = -np.inf
        children = []
        # currently is max player. Facing on 4 directions, you iterate, compare the heuristic,
        # choose the best direction to go.
        for action in self.ACTIONS:
            best_value = -np.inf
            board_copy = self.board * 1
            if can_move(board_copy, action):
                move(board_copy, action)
                best_value = self.basic_run(board_copy, self.max_depth, False)
            if best_value > max_value:
                best_move = action
        return best_move




    def basic_run(self, board, max_depth, is_max):
        if (max_depth == 0) or check_end(board):
            return self.eval(board)
        if is_max:
            best_value = -np.inf
            for action in self.ACTIONS:
                board_copy = board * 1
                if can_move(board_copy, action):
                    move(board_copy, action)
                    best_value = max(best_value, self.basic_run(board_copy, max_depth - 1, False))
            return best_value
        else:
            best_value = np.inf
            children = []
            empty_cells = find_empty_cells(board)
            for cell in empty_cells:
                board_copy = board * 1
                board_copy[cell[0]][cell[1]] = 2
                children.append(board_copy)
                board_copy = board * 1
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
        pass