import copy

from core.logic import *
from core.utils import *

keyboard_action = {'w': 'UP', 'W': 'UP', 's': 'DOWN', 'S': 'DOWN',
                   'a': 'LEFT', 'A': 'LEFT', 'd': 'RIGHT', 'D': 'RIGHT'}

def naive_random_move(board, curr_score, test_moves=100):
    """
    based on current board, and current score, return the next move
    four moves, randomly choose, and then take random moves until hit test_moves times or no longer survive
    compare scores of each direction, choose the largest one

    return value is one of action
    """

    moves = ('UP', 'DOWN', 'LEFT', 'RIGHT')

    successBoards = []

    scores = [curr_score for i in range(len(moves))]
    for i in range(len(moves)):
        action = moves[i]
        test_board = copy.deepcopy(board)

        if can_move(test_board, action):

            move(test_board, action)
            scores[i] = add_up(test_board, action, scores[i])
            # scores[i] += add_up_v2(test_board, action) 
            move(test_board, action)
            simple_add_num(test_board)


            total_runs = 0
            total_add_score = 0
            tmp_board = copy.deepcopy(test_board)
            for runs in range(test_moves):
                
                run_times = 1
                test_board = copy.deepcopy(tmp_board)
                
                while not check_end(test_board):
                    test_action = moves[random.randint(0, 3)]
                    # print("test for action", test_action, " in the ", test_times, " test times")
                    # print_board(test_board)
                    if can_move(test_board, test_action):

                        move(test_board, test_action)
                        # scores[i] = add_up(test_board, test_action, scores[i])
                        total_add_score += add_up_v2(test_board, test_action)                    
                        move(test_board, test_action)
                        simple_add_num(test_board)
                        run_times += 1
                
                total_runs += run_times
            # scores[i] = scores[i] / run_times
                if find_max_cell(test_board) > 4096:
                    successBoards.append(test_board)
            print("avg run times :", total_runs / test_moves)
            scores[i] += total_add_score / total_runs

    if max(scores) == curr_score:
        print("this time the AI can not make a move")
        return moves[random.randint(0, 3)], successBoards
    else:
        return moves[scores.index(max(scores))], successBoards

def run_naive_MCTS(N=4,test_moves=100):

    random.seed()

    board = make_board(N)
    initial_two(board)
    print_board(board)
    curr_score = 0

    stuck = 0
    human = False
    while not check_end(board):

        print(" ")
        print("current score is, ", curr_score)
        print("Possible actions: up, left, right, down, exit")
        if not human:
            action, successBoards = naive_random_move(
                board, curr_score, test_moves)
            if len(successBoards) > 0:
                c = input("find success board in test run, please press enter")
                for successBoard in successBoards:
                    print_board(successBoard)
                    print(" ")
                c = input("press enter to continue...")
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
            # curr_score = add_up(board, action, curr_score)
            curr_score += add_up_v2(board, action)
            move(board, action)
            clear()
            simple_add_num(board)
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
    print("Your Score is ", curr_score)
    print("Max number in board is", find_max_cell(board))
    print("Game end")
    return find_max_cell(board)


def human_run():
    board = make_board(4)
    initial_two(board)
    print_board(board)
    curr_score = 0
    while not check_end(board):
        print(" ")
        print("current score is, ", curr_score)
        print("Possible actions: up, left, right, down, exit")
        print("Please press WASD for UP LEFT DOWN RIGHT")
        action = keyboard_action[key_press()]
        action = action.upper()
        if action == "EXIT":
            break
        # take action here to do the move
        # and clear current , then print board
        if can_move(board, action):
            move(board, action)
            curr_score = add_up(board, action, curr_score)
            move(board, action)
            clear()
            simple_add_num(board)
            print_board(board)
        else:
            clear()
            print_board(board)
    print("")
    print("Game end")
    print("Your Score is ", curr_score)
    print("Max number in board is", find_max_cell(board))
    print("To run this game, type run()")


##############################################
# HELPER FUNCTION 
##############################################

def simple_add_num(board):
    """
    simple add a number in the board

    if tile has empty, find it, and then 
    90% add 2
    10% add 4

    """
    emptyCells = find_empty_cells(board)
    if len(emptyCells) == 0:
        print("no empty cells, return")
        return

    row, col = emptyCells[random.randint(0, len(emptyCells) - 1)]
    random.seed()
    p = random.random()
    if p < 0.9:
        board[row][col] = 2
    else:
        board[row][col] = 4
