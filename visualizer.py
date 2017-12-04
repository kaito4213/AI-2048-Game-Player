import numpy as np
import random
import plotly.plotly as py
import plotly.graph_objs as go
from core.gui import BACKGROUND_COLOR_DICT
import colorlover as cl
import math

def test_generator(n):
    '''
    Generate a list contains n dictionaries.
    {"movements: 1111,
         "score": 111,
        "max_tile": 2048,
        "depth": 2}
    :param n:
    :return: a list of dictionary
    '''
    lst = []
    for i in range(n):
        temp = {}
        for j in ["movements", "score", "depth"]:
            temp[j] = random.randint(1,1000)
        temp["max_tile"] = random.choice(list(BACKGROUND_COLOR_DICT.keys()))
        lst.append(temp)
    return lst


def dict_txt_parser(path):
    import ast
    import json
    lst = []
    with open(path, 'r') as f:
        s = f.readlines()
        for line in s:
            whip = ast.literal_eval(line)
            lst.append(whip)
    print("The length of data is {}".format(len(lst)))
    return lst


class Visualizer:
    def __init__(self, x_range = np.arange(1, 50)):
        '''

        :param x_range: The range of x
        '''
        self.x_range = x_range
        self.dataset = {}

    def add_data(self, label, data):
        '''
        :param label: a str identify the name of the data.
        :param data: should be a 1D array that  has the same length to x_range
        :return: None
        '''
        if len(data) != len(self.x_range):
            Warning("The length of data is {}, which is not the same as the length of x: {}".format(len(data), len(self.x_range)))
            if len(data)< len(self.x_range):
                for i in range(len(self.x_range) - len(data)):
                    data.append(0)
            else:
                data = data[:len(self.x_range)]
        self.dataset[label] = data

    def get_value_by_key(self, key):
        lst = []
        labels = []
        for label in self.dataset:
            temp = []
            labels.append(label)
            for unit in self.dataset[label]:
                temp.append(unit[key])
            lst.append(temp)
        return lst, labels

    def get_max(self, matrix):
        '''
        For each row in matrix, get the max in each row
        :param matrix:
        :return:
        '''
        max_lst = []
        for row in matrix:
            max_lst.append(max(row))
        return max_lst

    def get_average(self, matrix):
        av_lst = []
        for row in matrix:
            av_lst.append(np.average(row))
        return av_lst

    def draw_lines(self, key):
        lines = []
        data_of_key, labels = self.get_value_by_key(key)
        for i in range(len(data_of_key)):
            trace = go.Scatter(
                x= self.x_range,
                y= data_of_key[i],
                mode='lines+markers',
                name=labels[i]
            )
            lines.append(trace)
        layout = dict(title = "{} for Different Algorithms".format(key),
                      xaxis = dict(title = "Run Time"),
                      yaxis = dict(title = key))
        fig = dict(data = lines, layout = layout)
        return py.iplot(fig, filename = "Line of {}".format(key))

    def draw_grouped_bar(self, key):
        data_of_key, labels = self.get_value_by_key(key)
        best_lst = self.get_max(data_of_key)
        aver_lst = self.get_average(data_of_key)

        trace0 = go.Bar(
            x=labels,
            y=best_lst,
            name='Best {}'.format(key)
        )

        trace1 = go.Bar(
            x=labels,
            y=aver_lst,
            name='Average {}'.format(key)
        )
        bars = [trace0, trace1]
        layout = go.Layout(
            barmode = 'group',
            title = "{} for Different Algorithms".format(key),
            yaxis=dict(title=key)
        )
        fig = dict(data = bars, layout = layout)
        return py.iplot(fig, filename = "Line of {}".format(key))

    def draw_stack_bar(self, key):
        count_matrix = []
        data_of_key, labels = self.get_value_by_key(key)
        all_uniques_cells = sorted(list(BACKGROUND_COLOR_DICT.keys()))
        for i in range(len(data_of_key)):
            uniques, counts = np.unique(data_of_key[i], return_counts= True)
            temp = []

            # sum_counts = np.sum(counts)
            # counts = counts/sum_counts
            i = 0
            print(uniques, all_uniques_cells)
            for j in all_uniques_cells:
                if i >= len(uniques):
                    temp.append(0)
                elif j == uniques[i]:
                    temp.append(counts[i])
                    i += 1
                else:
                    temp.append(0)

            count_matrix.append(temp)
        np_matrix = np.array(count_matrix)
        np_matrix = np_matrix.T
        bupu = cl.scales['9']['seq']['YlOrBr']
        bupux = cl.interp(bupu, 100)
        gap = math.floor(100/len(np_matrix))
        stacked_data = []
        for i in range(len(np_matrix)):
            trace0 = go.Bar(
                x = labels,
                y = np_matrix[i],
                name = all_uniques_cells[i],
                marker = dict(
                    # cmax=len(np_matrix),
                    # cmin=0,
                    # colorscale='Viridis',
                    color = bupux[gap * i]
                )
            )
            stacked_data.append(trace0)

        layout = go.Layout(
            barmode = 'stack'
        )
        fig = go.Figure(data=stacked_data, layout=layout)
        return py.iplot(fig, filename='stacked-bar')



