
# main script

from time import sleep

from player import initialize_prob_mines, prob_update, player_moves
from board import Board
from board_eval import find_bombs

# parameters ########################
rows = 8
cols = rows
mines = 10

lag = 1    # seconds after printing

# setup and first move ########################
while True:
    my_board = Board(rows, cols, mines)
    prob_mines = initialize_prob_mines(my_board)

    my_board.move(3, 3)
    prob_mines[3][3] = 0

    # for now, testing only games that start well
    if my_board.reveal(3,3) == 0:
        break

print(my_board)


# gameplay ########################
while True:
    # initial probabilities
    prob_mines = basic_updater(prob_mines, my_board)
    prob_mines = bomb_finder(prob_mines, my_board)

    # start by flagging
    print('Flagging bombs')

    sleep(lag)
    for i in range(my_board.rows):
        for j in range(my_board.cols):
            label = my_board.reveal(i, j)
            if prob_mines[i][j] == 1 and label != my_board.flag_icon:
                my_board.flag(i, j)
                print(my_board)
                sleep(lag)

    # probabilties agains
    prob_mines = basic_updater(prob_mines, my_board)
    prob_mines = bomb_finder(prob_mines, my_board)

    # now make moves
    print('Making moves')
    sleep(lag)

    moves = player_moves(prob_mines, my_board)

    print('%i safe move(s) exist(s)' % len(moves))
    sleep(lag)

    if not moves:
        break

    for [i, j] in moves:
        if my_board.reveal(i, j) == my_board.unknown_icon:
            my_board.move(i, j)
            print(my_board)
            sleep(lag)
