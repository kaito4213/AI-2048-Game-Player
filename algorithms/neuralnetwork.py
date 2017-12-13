#Acknowledgement:
# The code mainly comes from the following link.
# https://github.com/tjwei/2048-NN/blob/master/my2048-rl-theano-n-tuple-Copy7.ipynb

import numpy as np
import theano
import theano.tensor as T
import lasagne
import copy as cp
from core.logic import can_move, check_end, move, add_up_v2, simple_add_num
from core.utils import Actions, replace_star, print_board, find_max_cell, tile_count
from manager import make_board, initial_two
from lasagne.layers import DenseLayer, InputLayer, DropoutLayer
from lasagne.layers import MergeLayer, ReshapeLayer, FlattenLayer, ConcatLayer
from lasagne.nonlinearities import rectify, softmax, sigmoid
from lasagne.init import Constant, Sparse
from lasagne.layers import Conv2DLayer
from lasagne.regularization import regularize_network_params, l1, l2, regularize_layer_params_weighted
floatX = theano.config.floatX

input_var = T.tensor4()
target_var = T.vector()
N_FILTERS = 512
N_FILTERS2 = 4096

_ = InputLayer(shape=(None, 16, 4, 4), input_var=input_var)

conv_a =  Conv2DLayer(_, N_FILTERS, (2,1), pad='valid')#, W=Winit((N_FILTERS, 16, 2, 1)))
conv_b =  Conv2DLayer(_, N_FILTERS, (1,2), pad='valid')#, W=Winit((N_FILTERS, 16, 1, 2)))

conv_aa =  Conv2DLayer(conv_a, N_FILTERS2, (2,1), pad='valid')#, W=Winit((N_FILTERS2, N_FILTERS, 2, 1)))
conv_ab =  Conv2DLayer(conv_a, N_FILTERS2, (1,2), pad='valid')#, W=Winit((N_FILTERS2, N_FILTERS, 1, 2)))

conv_ba =  Conv2DLayer(conv_b, N_FILTERS2, (2,1), pad='valid')#, W=Winit((N_FILTERS2, N_FILTERS, 2, 1)))
conv_bb =  Conv2DLayer(conv_b, N_FILTERS2, (1,2), pad='valid')#, W=Winit((N_FILTERS2, N_FILTERS, 1, 2)))

_ = ConcatLayer([FlattenLayer(x) for x in [conv_aa, conv_ab, conv_ba, conv_bb, conv_a, conv_b]])
l_out = DenseLayer(_, num_units=1,  nonlinearity=None)

prediction = lasagne.layers.get_output(l_out)
P = theano.function([input_var], prediction)
loss = lasagne.objectives.squared_error(prediction, target_var).mean()/2

accuracy = lasagne.objectives.squared_error(prediction, target_var).mean()
params = lasagne.layers.get_all_params(l_out, trainable=True)

updates = lasagne.updates.adam(loss, params, beta1=0.5)

train_fn = theano.function([input_var, target_var], loss, updates=updates)
loss_fn = theano.function([input_var, target_var], loss)
accuracy_fn =theano.function([input_var, target_var], accuracy)


table = {2**i:i for i in range(1,16)}
table[0]=0


def vchange(board, v):
    g0 = board
    g1 = g0[:, ::-1, :]
    g2 = g0[:, :, ::-1]
    g3 = g2[:, ::-1, :]
    r0 = board.swapaxes(1, 2)
    r1 = r0[:, ::-1, :]
    r2 = r0[:, :, ::-1]
    r3 = r2[:, ::-1, :]
    xtrain = np.array([g0, g1, g2, g3, r0, r1, r2, r3], dtype=floatX)
    ytrain = np.array([v] * 8, dtype=floatX)
    train_fn(xtrain, ytrain)


def make_input(board):
    g0 = np.array(replace_star(board))

    r = np.zeros(shape=(16, 4, 4), dtype=floatX)
    for i in range(4):
        for j in range(4):
            v = g0[i, j]
            r[table[v], i, j] = 1
    return r


def train_nn():
    board = make_board(4)
    initial_two(board)
    print_board(board)
    curr_score = 0
    game_len = 0
    last_grid = None
    while not check_end(board):
        board_list = []
        for action in Actions:
            board_copy = cp.deepcopy(board)
            if can_move(board_copy, action):
                move(board_copy, action)
                score = add_up_v2(board_copy,action)
                move(board_copy, action)
                board_list.append((board_copy, action, score))
        if board_list:
            boards = np.array([make_input(g) for g, m, s in board_list], dtype=floatX)
            p = P(boards).flatten()
            game_len += 1
            print(game_len)
            best_move = -1
            best_v = None
            for i, (g,m,s) in enumerate(board_list):
                v = 2*s + p[i]
                if best_v is None or v > best_v:
                    best_v = v
                    best_move = m
                    best_score = 2*s
                    best_grid = boards[i]
            move(board, best_move)
            curr_score += add_up_v2(board, best_move)
            move(board, best_move)
            simple_add_num(board)
            print_board(board)
        else:
            best_v = 0
            best_grid = None
        if last_grid is not None:
            vchange(last_grid, best_v)
        last_grid = best_grid

    return game_len, find_max_cell(board), curr_score, board

def get_NN_result():
    res_single = []
    for i in range(200):
        board_info = {}
        game_len, max_tile, curr_score, result_board =  train_nn()
        tile_counts = tile_count(result_board)
        board_info['movements'] =game_len
        board_info['score'] = curr_score
        board_info['max_tile'] = max_tile
        board_info['tile_count'] = tile_counts

        res_single.append(board_info)

        with open('results_{}_{}.txt'.format("neural_network", 'single_count'), mode='wt',
                  encoding='utf-8') as out:
            for e in res_single:
                out.write(str(e))
                out.write('\n')

        return res_single


get_NN_result()