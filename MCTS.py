from logic import *
from utils import *
from Game_Manager import initial_two, place_two

import time
import random
import copy

moves = ('UP', 'DOWN', 'LEFT', 'RIGHT')

def naive_random_move(board, curr_score, test_moves=100):
    """
    based on current board, and current score, return the next move
    four moves, randomly choose, and then take random moves until hit test_moves times or no longer survive
    compare scores of each direction, choose the largest one

    return value is one of action
    """
    
    scores = [curr_score for i in range(len(moves))]
    for i in range(len(moves)):
        action = moves[i]
        test_board = copy.deepcopy(board)
        
        if can_move(test_board,action):
            
            move(test_board, action)
            scores[i] = add_up(test_board, action,scores[i])
            move(test_board, action)

            test_times = test_moves
            while test_times >= 0 and not check_end(test_board):
                test_action = moves[random.randint(0,3)]
                if can_move(test_board,test_action):
                    move(test_board,test_action)
                    scores[i] = add_up(test_board,test_action,scores[i])
                    move(test_board,test_action)
                test_times -= 1
    if max(scores) == curr_score:
        return moves[random.randint(0,3)]
    else:
        return moves[scores.index(max(scores))]

def run_naive_MCTS(test_moves=50):
    board = make_board(4)
    initial_two(board)
    print_board(board)
    curr_score = 0

    stuck = 0
    human = False
    while not check_end(board):
        
        print(" ")
        print("current score is, ",curr_score)
        print("Possible actions: up, left, right, down, exit")
        if not human:
            action = naive_random_move(board,curr_score,test_moves)
            action = action.upper()
        else:
            print("AI stuck, need human help ")
            print("Possible actions: up, left, right, down, exit")
            action = input('Your action: ')
            action = action.upper()
            human = False

        if action == "EXIT":
            break
        # take action here to do the move
        # and clear current , then print board
        if can_move(board, action):
            move(board, action)
            curr_score = add_up(board, action,curr_score)
            move(board, action)
            clear()
            place_two(board)
            print_board(board)
            print(" ")
        else:
            stuck += 1
            # clear()
            # print_board(board)
            print("action is ", action, " but can not move")
            if stuck >= 10:
                clear()
                print_board(board) 
                stuck = 0
                human = True

        # time.sleep(0.2)

    print("Game end")