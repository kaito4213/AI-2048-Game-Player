# different kinds of evaluations
# May be used in different heuristic functions

import math


class Evaluator:
    def __init__(self, board):
        self.board = board


class MinimaxEvaluator(Evaluator):
    def __init__(self, board):
        Evaluator.__init__(self, board)

    def smoothness(self):
        """
        measures how smooth the grid is
        Sums of the pairwise difference between neighboring tiles (in log space, so it represents the
        number of merges that need to happen before they can merge).
        """

        N = len(self.board)
        res = 0
        for i in range(N):
            for j in range(N):
                if self.board[i][j] != '*':
                    curr_value = math.log(self.board[i][j],2)
                    for direction in ('RIGHT', 'DOWN'):
                        next_num_cell = self.find_first_non_empty_cell(i,j, direction)
                        if next_num_cell != None:
                            x, y = next_num_cell
                            next_num_value = math.log(self.board[x][y],2)
                            res -= abs(curr_value - next_num_value)
        return res

    def monotonicity(self):
        """
        measure the monotonicity of the board
        """

        N = len(self.board)

        # score[0]: up/down direction, increasing
        # score[1]: up/down direction, decreasing
        # score[2]: left/right direction, increasing
        # score[3]: left/right direction, decreasing
        score = [0,0,0,0]

        # up/down direction
        for row in range(N):
            curr_cell = 0
            while curr_cell < N and self.board[row][curr_cell] == '*':
                curr_cell += 1
            next_cell = curr_cell + 1
            while next_cell < N:
                while next_cell < N and self.board[row][next_cell] == '*':
                    next_cell += 1

                if next_cell < N:
                    if self.board[row][curr_cell] > self.board[row][next_cell]:
                        score[0] += self.board[row][next_cell] - self.board[row][curr_cell]
                    elif self.board[row][curr_cell] < self.board[row][next_cell]:
                        score[1] += self.board[row][curr_cell] - self.board[row][next_cell]

                curr_cell = next_cell
                next_cell += 1

        # left/right direction
        for col in range(N):
            curr_cell = 0
            while curr_cell < N and self.board[curr_cell][col] == '*':
                curr_cell += 1
            next_cell = curr_cell + 1
            while next_cell < N:
                while next_cell < N and self.board[next_cell][col] == '*':
                    next_cell += 1

                if next_cell < N:
                    if self.board[curr_cell][col] > self.board[next_cell][col]:
                        score[2] += self.board[next_cell][col] - self.board[curr_cell][col]
                    elif self.board[curr_cell][col] < self.board[next_cell][col]:
                        score[3] += self.board[curr_cell][col] - self.board[next_cell][col]

                curr_cell = next_cell
                next_cell += 1

        return max(score[0], score[1]) + max(score[2],score[3])

    def emptiness(self):
        """
        measure how empty the board is
        simply return the number of empty board
        """
        N = len(self.board)

        count = 0
        for i in range(N):
            for j in range(N):
                if self.board[i][j] == '*':
                    count += 1
        return count

    def max_val(self):
        """
        find the max value of the board

        Duplicate with utils.find_max_cell
        """
        N = len(self.board)
        res = 0
        for i in range(N):
            for j in range(N):
                if self.board[i][j] != '*' and self.board[i][j] > res:
                    res = self.board[i][j]

        return res

    def find_first_non_empty_cell(self, row, col, direction='RIGHT'):
        ###################
        # HELPER FUNCTION #
        ###################
        """
        Find the first non empty cell on the board based on the current positoin
        Only find in two directions: RIGHT and DOWN
        if find, return position, else, return None
        """
        N = len(self.board)

        if direction.upper() == 'RIGHT':
            # find in the same row:
            for k in range(col, N):
                if self.board[row][k] != '*':
                    return row, k

        elif direction.upper() == 'DOWN':
            # find in the same col
            for k in range(row, N):
                if self.board[k][col] != '*':
                    return k, col

        return None