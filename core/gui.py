# The code mainly comes from https://github.com/yangshun/2048-python/blob/master/puzzle.py
import copy
import threading
import numpy as np
import time
from random import *
from tkinter import *
from sys import platform
from algorithms.MCTS import naive_random_move
from algorithms.expectimax import expectimax
from algorithms.minimax import Minimax
from core.utils import *
from core.logic import *


SIZE = 500
GRID_LEN = 4
GRID_PADDING = 8

BACKGROUND_COLOR_GAME = "#92877d"
BACKGROUND_COLOR_CELL_EMPTY = "#9e948a"
BACKGROUND_COLOR_DICT = {2: "#eee4da", 4: "#ede0c8", 8: "#f2b179", 16: "#f59563",
                         32: "#f67c5f", 64: "#f65e3b", 128: "#edcf72", 256: "#edcc61",
                         512: "#edc850", 1024: "#edc53f", 2048: "#edc22e", 4096:"#edc22e", 8192:"#eff9c5",16384:"#11f29c"}
CELL_COLOR_DICT = {2: "#776e65", 4: "#776e65", 8: "#f9f6f2", 16: "#f9f6f2",
                   32: "#f9f6f2", 64: "#f9f6f2", 128: "#f9f6f2", 256: "#f9f6f2",
                   512: "#f9f6f2", 1024: "#f9f6f2", 2048: "#f9f6f2", 4096: "#f9f53e", 8192:"#f9f6f3",16384:"#f9f6f3"}
FONT = ("Verdana", 20, "bold")

MOVES = ('UP', 'DOWN', 'LEFT', 'RIGHT')

class GameGrid(Frame):
    def __init__(self, AI_mode=True, which_AI = 'minimax'):
        Frame.__init__(self)
        self.actions = {'w': 'UP', 'W': 'UP', 's': 'DOWN', 'S': 'DOWN',
                         'a': 'LEFT', 'A': 'LEFT', 'd': 'RIGHT', 'D': 'RIGHT'}
        self.grid()
        self.master.title('2048 Player - CS534 Final Project')
        self.master.bind("<Key>", self.key_down)
        self.grid_cells = []
        self.init_matrix()
        self.init_grid()
        self.init_score()
        self.update_score()
        self.update_grid_cells()

        if AI_mode:
            if platform == 'win32' or platform == 'cygwin':
                class clipboardthread(threading.Thread):
                    def __init__(self):
                        threading.Thread.__init__(self)

                    def run(self):
                        clipboardcheck()

                def clipboardcheck():
                    if which_AI.upper() == 'EXPECTIMAX':
                        self.expectimax_AI_run()
                    elif which_AI.upper() == 'MCTS':
                        self.simple_mcts_AI_run()
                    elif which_AI.upper() == "MINIMAX":
                        self.minimax_run()
                    elif which_AI.upper() == "MINIMAX_PRUNING":
                        self.minimax_pruning_run()
                clipboardthread.daemon = True

                clipboardthread().start()
            else:
                if which_AI.upper() == 'EXPECTIMAX':
                    self.expectimax_AI_run()
                elif which_AI.upper() == 'MCTS':
                    self.simple_mcts_AI_run()
                elif which_AI.upper() == "MINIMAX":
                    self.minimax_run()
                elif which_AI.upper() == "MINIMAX_PRUNING":
                    self.minimax_pruning_run()
        self.mainloop()

    def init_score(self):
        footer_label = Frame(self.background, bg=BACKGROUND_COLOR_CELL_EMPTY, width=SIZE/2, height=50)
        footer_label.grid(row = GRID_LEN, column = 0, columnspan = 2, padx=GRID_PADDING, pady=GRID_PADDING)
        title_cell = Label(master=footer_label, text="Score:", bg=BACKGROUND_COLOR_DICT[2], justify=CENTER, font=FONT, width=10,
                  height=2)
        title_cell.grid()
        footer_score = Frame(self.background, bg=BACKGROUND_COLOR_CELL_EMPTY, width=SIZE/2, height=50)
        footer_score.grid(row = GRID_LEN, column = 2, columnspan = 2, padx=GRID_PADDING, pady=GRID_PADDING)
        self.score_cell = Label(master=footer_score, text=self.score, bg=BACKGROUND_COLOR_DICT[2], justify=CENTER, font=FONT, width=10,
                  height=2)
        self.score_cell.grid()


    def init_grid(self):
        self.background = Frame(self, bg=BACKGROUND_COLOR_GAME, width=SIZE, height=SIZE+50)
        self.background.grid()
        for i in range(GRID_LEN):
            grid_row = []
            for j in range(GRID_LEN):
                cell = Frame(self.background, bg=BACKGROUND_COLOR_CELL_EMPTY, width=SIZE / GRID_LEN, height=SIZE / GRID_LEN)
                cell.grid(row=i, column=j, padx=GRID_PADDING, pady=GRID_PADDING)
                # font = Font(size=FONT_SIZE, family=FONT_FAMILY, weight=FONT_WEIGHT)
                t = Label(master=cell, text="", bg=BACKGROUND_COLOR_CELL_EMPTY, justify=CENTER, font=FONT, width=4,
                          height=2)
                t.grid()
                grid_row.append(t)

            self.grid_cells.append(grid_row)

    def gen(self):
        return randint(0, GRID_LEN - 1)

    def init_matrix(self):
        self.matrix = make_board(4)
        initial_two(self.matrix)
        self.score = 0

    def update_grid_cells(self):
        for i in range(GRID_LEN):
            for j in range(GRID_LEN):
                new_number = self.matrix[i][j]
                if new_number == '*':
                    self.grid_cells[i][j].configure(text="", bg=BACKGROUND_COLOR_CELL_EMPTY)
                else:
                    self.grid_cells[i][j].configure(text=str(new_number), bg=BACKGROUND_COLOR_DICT[new_number],
                                                    fg=CELL_COLOR_DICT[new_number])
        self.update_idletasks()

    def update_score(self):
        self.score_cell.configure(text=self.score)


    def key_down(self, event):
        key = repr(event.char).replace("'", "")
        if key in self.actions:
            action = self.actions[key]
            if can_move(self.matrix, action):
                move(self.matrix, action)
                self.score += add_up_v2(self.matrix, action)
                move(self.matrix, action)
                simple_add_num(self.matrix)
                self.update_score()
                self.update_grid_cells()
                if check_end(self.matrix):
                    self.grid_cells[1][1].configure(text="Game", bg=BACKGROUND_COLOR_CELL_EMPTY)
                    self.grid_cells[1][2].configure(text="Over!", bg=BACKGROUND_COLOR_CELL_EMPTY)

    def generate_next(self):
        index = (self.gen(), self.gen())
        while self.matrix[index[0]][index[1]] != "*":
            index = (self.gen(), self.gen())
        self.matrix[index[0]][index[1]] = 2

    def simple_mcts_AI_run(self):
        while not check_end(self.matrix):
            action, successBoards = naive_random_move(self.matrix,self.score,test_moves=30)
            if can_move(self.matrix,action):
                move(self.matrix, action)
                self.score += add_up_v2(self.matrix, action)
                move(self.matrix, action)
                self.update_score()
                self.update_grid_cells()
                simple_add_num(self.matrix)
                self.update_grid_cells()
                # if check_end(self.matrix):
                #     self.grid_cells[1][1].configure(text="Game", bg=BACKGROUND_COLOR_CELL_EMPTY)
                #     self.grid_cells[1][2].configure(text="Over!", bg=BACKGROUND_COLOR_CELL_EMPTY)

    def expectimax_AI_run(self):
        while not check_end(self.matrix):

            depth = 2
            best_move = None
            best_val = -1

            for direction in MOVES:
                if not can_move(self.matrix, direction):
                    # clear()
                    continue

                temp_board = copy.deepcopy(self.matrix)
                move(temp_board, direction)
                add_up(temp_board, direction, 0)
                move(temp_board, direction)

                alpha = expectimax(temp_board, depth)
                if best_val < alpha:
                    best_val = alpha
                    best_move = direction

            move(self.matrix,best_move)
            self.score += add_up_v2(self.matrix, best_move)
            move(self.matrix,best_move)
            self.update_score()
            self.update_grid_cells()
            simple_add_num(self.matrix)
            self.update_grid_cells()

    def minimax_run(self):
        while not check_end(self.matrix):
            mm = Minimax(board= self.matrix, max_depth= 5)
            best_move = mm.basic_move()
            if can_move(self.matrix, best_move):
                move(self.matrix, best_move)
                self.score +=add_up_v2(self.matrix, best_move)
                move(self.matrix, best_move)
                self.update_score()
                self.update_grid_cells()
                simple_add_num(self.matrix)
                self.update_grid_cells()
                # time.sleep(0.1)
                # if check_end(self.matrix):
                #     self.grid_cells[1][1].configure(text="Game", bg=BACKGROUND_COLOR_CELL_EMPTY)
                #     self.grid_cells[1][2].configure(text="Over!", bg=BACKGROUND_COLOR_CELL_EMPTY)

    def minimax_pruning_run(self):
        while not check_end(self.matrix):
            mm = Minimax(board= self.matrix, max_depth= 4)
            best_move = mm.alpha_beta_move()
            if can_move(self.matrix, best_move):
                move(self.matrix, best_move)
                self.score +=add_up_v2(self.matrix, best_move)
                move(self.matrix, best_move)
                self.update_score()
                self.update_grid_cells()
                simple_add_num(self.matrix)
                self.update_grid_cells()
                # time.sleep(0.1)
                # if check_end(self.matrix):
                    # self.grid_cells[1][1].configure(text="Game", bg=BACKGROUND_COLOR_CELL_EMPTY)
                    # self.grid_cells[1][2].configure(text="Over!", bg=BACKGROUND_COLOR_CELL_EMPTY)

    # def neural_netword_run(self):
    #     while not check_end(self.matrix):
    #         nn = NeuralNetwork(board= self.matrix)
    #         best_move = nn.alpha_beta_move()
    #         if can_move(self.matrix, best_move):
    #             move(self.matrix, best_move)
    #             self.score +=add_up_v2(self.matrix, best_move)
    #             move(self.matrix, best_move)
    #             self.update_score()
    #             self.update_grid_cells()
    #             simple_add_num(self.matrix)
    #             self.update_grid_cells()