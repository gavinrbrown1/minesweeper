
# main script

from time import sleep, time

from player import initialize_prob_mines, prob_update, player_moves, safe_spaces
from board import Board
from board_eval import done

# parameters ########################
rows = 8
cols = rows
mines = 10

lag = 1    # seconds after printing

verbose = False

won_games = 0
total_games = 100
# move_counts = []

for i in range(total_games):
    # move_counter = 0

# setup and first move ########################
    while True:
        my_board = Board(rows, cols, mines)
        prob_mines = initialize_prob_mines(my_board)

        my_board.move(3, 3)
        prob_mines[3][3] = 0

        if verbose:
            print('Initial board')
            print(my_board)
            sleep(lag)

        if my_board.reveal(3,3) != my_board.mine_icon:
            break


    # gameplay ########################
    while True:
        # initial probabilities
        prob_mines = prob_update(prob_mines, my_board)

        # start by flagging what we know is bombs
        for [i, j] in my_board.coords:
            label = my_board.reveal(i, j)
            if prob_mines[i][j] == 1 and label != my_board.flag_icon:
                my_board.flag(i, j)
                # print(my_board)
                # sleep(lag)

        if verbose:
            print('Flagging bombs')
            print(my_board)
            sleep(lag)

        # probabilties agains
        prob_mines = prob_update(prob_mines, my_board)

        # where is safe? Move there
        prob_mines = safe_spaces(prob_mines, my_board)

        if verbose:
            print('Making safe moves')

        made_moves = False

        for [i, j] in my_board.coords:
            label = my_board.reveal(i, j)
            if prob_mines[i][j] == 0 and label == my_board.unknown_icon:
                my_board.move(i, j)
                # move_counter += 1
                if my_board.reveal(i, j) == my_board.mine_icon:
                    print('fuck')
                if verbose:
                    print(my_board)
                    sleep(lag)

                made_moves = True

        if not made_moves:
            if verbose:
                print('No safe moves to make')

            # pick the first place that we don't know about
            lost = False

            for [i, j] in my_board.coords:
                if my_board.reveal(i, j) == my_board.unknown_icon:
                    my_board.move(i, j)
                    if verbose:
                        print(my_board)
                        sleep(lag)
                    if my_board.reveal(i, j) == my_board.mine_icon:
                        lost = True
                    break

            if lost:
                break


        if done(my_board):
            won_games += 1
            break

        # move_counts.append(move_counter)

print('Played %i games' % total_games)
print('Won %i games' % won_games)
print('Total win percentage: %.1f%%' % (100 * won_games / total_games))

# print('Printing expected win percentage for first ten moves')
