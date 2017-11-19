# The code mainly comes from https://github.com/yangshun/2048-python/blob/master/puzzle.py
from tkinter import *
from logic import *
from random import *
from game_manager import *
from sys import platform
import keyboard
import reprlib
import threading
from MCTS import naive_random_move

SIZE = 500
GRID_LEN = 4
GRID_PADDING = 10

BACKGROUND_COLOR_GAME = "#92877d"
BACKGROUND_COLOR_CELL_EMPTY = "#9e948a"
BACKGROUND_COLOR_DICT = {2: "#eee4da", 4: "#ede0c8", 8: "#f2b179", 16: "#f59563",
                         32: "#f67c5f", 64: "#f65e3b", 128: "#edcf72", 256: "#edcc61",
                         512: "#edc850", 1024: "#edc53f", 2048: "#edc22e"}
CELL_COLOR_DICT = {2: "#776e65", 4: "#776e65", 8: "#f9f6f2", 16: "#f9f6f2",
                   32: "#f9f6f2", 64: "#f9f6f2", 128: "#f9f6f2", 256: "#f9f6f2",
                   512: "#f9f6f2", 1024: "#f9f6f2", 2048: "#f9f6f2"}
FONT = ("Verdana", 40, "bold")




class GameGrid(Frame):
    def __init__(self, AI_mode=True):
        Frame.__init__(self)
        self.actions = {'w': 'UP', 'W': 'UP', 's': 'DOWN', 'S': 'DOWN',
                         'a': 'LEFT', 'A': 'LEFT', 'd': 'RIGHT', 'D': 'RIGHT'}
        self.grid()
        self.master.title('2048 Player - CS534 Final Project')
        self.master.bind("<Key>", self.key_down)
        self.grid_cells = []
        self.init_grid()
        self.init_matrix()
        self.update_grid_cells()

        if AI_mode:

            if platform == 'win32' or platform == 'cygwin':
                class clipboardthread(threading.Thread):
                    def __init__(self):
                        threading.Thread.__init__(self)

                    def run(self):
                        clipboardcheck()

                def clipboardcheck():
                    self.simple_mcts_AI_run()
                clipboardthread.daemon = True

                clipboardthread().start()
            else:
                self.simple_mcts_AI_run()
        self.mainloop()


    def init_grid(self):
        background = Frame(self, bg=BACKGROUND_COLOR_GAME, width=SIZE, height=SIZE)
        background.grid()
        for i in range(GRID_LEN):
            grid_row = []
            for j in range(GRID_LEN):
                cell = Frame(background, bg=BACKGROUND_COLOR_CELL_EMPTY, width=SIZE / GRID_LEN, height=SIZE / GRID_LEN)
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

    def key_down(self, event):
        key = repr(event.char).replace("'", "")
        if key in self.actions:
            action = self.actions[key]
            if can_move(self.matrix, action):
                move(self.matrix, action)
                self.score = add_up(self.matrix, action, self.score)
                simple_add_num(self.matrix)
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
                simple_add_num(self.matrix)
                self.update_grid_cells()
                if check_end(self.matrix):
                    self.grid_cells[1][1].configure(text="Game", bg=BACKGROUND_COLOR_CELL_EMPTY)
                    self.grid_cells[1][2].configure(text="Over!", bg=BACKGROUND_COLOR_CELL_EMPTY)



gamegrid = GameGrid(AI_mode=True)