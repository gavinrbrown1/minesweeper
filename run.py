
# main script

from time import sleep, time

from player import initialize_prob_mines, prob_update, player_moves, safe_spaces
from board import Board
from board_eval import find_bombs

# parameters ########################
rows = 8
cols = rows
mines = 10

lag = 2    # seconds after printing

verbose = False

# setup and first move ########################
while True:
    my_board = Board(rows, cols, mines)
    prob_mines = initialize_prob_mines(my_board)

    my_board.move(3, 3)
    prob_mines[3][3] = 0

    # for now, testing only games that start well
    if my_board.reveal(3,3) == 0:
        break

if verbose:
    print('Initial board')
    print(my_board)
    sleep(lag)

# gameplay ########################

while True:
    # initial probabilities
    prob_mines = prob_update(prob_mines, my_board)

    # start by flagging what we know is bombs
    for i in range(my_board.rows):
        for j in range(my_board.cols):
            label = my_board.reveal(i, j)
            if prob_mines[i][j] == 1 and label != my_board.flag_icon:
                my_board.flag(i, j)
                # print(my_board)
                # sleep(lag)

    if verbose:
        print('Flagging bombs')
        print(my_board)
        sleep(2 * lag)

    # probabilties agains
    prob_mines = prob_update(prob_mines, my_board)

    # where is safe? Move there
    prob_mines = safe_spaces(prob_mines, my_board)

    if verbose:
        print('Making safe moves')

    made_moves = False

    for i in range(my_board.rows):
        for j in range(my_board.cols):
            label = my_board.reveal(i, j)
            if prob_mines[i][j] == 0 and label == my_board.unknown_icon:
                my_board.move(i, j)
                if my_board.reveal(i, j) == my_board.mine_icon:
                    print('fuck')
                if verbose:
                    print(my_board)
                    sleep(lag)

                made_moves = True

    if not made_moves:
        if verbose:
            print('No safe moves to make')
        break
