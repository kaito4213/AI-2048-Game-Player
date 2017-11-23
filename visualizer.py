import matplotlib.pyplot as plt
import manager
import numpy as np

class Visualizer:
    def __init__(self, run_time = 2, mode = "score", algo = "expectimax"):
        self.score_lst = []
        self.cell_lst = []
        self.x = []
        self.run_time = run_time
        self.mode = mode
        self.algo = algo

    def processing(self):
        for i in range(self.run_time):
            best_score, max_cell = manager.run(mode = self.mode, algo = self.algo)
            self.score_lst.append(best_score)
            self.cell_lst.append(max_cell)
            self.x.append(i+1)
        # Count the frequency of max cell value
        self.unique_cell, self.unique_count = np.unique(self.cell_lst)

    def get_score(self):
        return np.average(self.score_lst)

    def visualize(self):
        plt.hist(self.unique_cell, self.unique_count, facecolor = "g", alpha = 0.75)
        plt.xlabel("Max Cell")
        plt.ylabel("Counts")
        plt.show()

a = Visualizer()
a.processing()
a.visualize()