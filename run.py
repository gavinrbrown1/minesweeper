
# main script

from time import sleep, time

from player import initialize_prob_mines, prob_update, player_moves, safe_spaces, print_probs, pull_neighbors, uncertain_mover
from board import Board
from board_eval import done

# parameters ########################
rows = 16
cols = 30
mines = 99

lag = 1    # seconds after printing

verbose = True

won_games = 0
total_games = 10
# move_counts = []

# first moves
init_row = 7
init_col = 14

# setup and gameplay ########################

start = time()
for i in range(total_games):
    # move_counter = 0

    my_board = Board(rows, cols, mines)
    prob_mines = initialize_prob_mines(my_board)

    my_board.move(init_row, init_col)
    prob_mines[init_row][init_col] = 0

    if verbose:
        print('Initial board')
        print(my_board)
        sleep(lag)

    if my_board.reveal(init_row, init_col) != my_board.mine_icon:
        # if we hit a mine on the first go, oh well


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
                        print('fuck, you were confident but still hit a mine')
                    if verbose:
                        print(my_board)
                        # print_probs(prob_mines)
                        sleep(lag)

                    made_moves = True

            if not made_moves:
                if verbose:
                    print('No safe moves to make')

                lost = False

                # returns a choice
                [i, j] = uncertain_mover(prob_mines, my_board)

                my_board.move(i, j)
                if verbose:
                    print(my_board)
                    sleep(lag)
                if my_board.reveal(i, j) == my_board.mine_icon:
                    lost = True

                if lost:
                    break


            if done(my_board):
                won_games += 1
                break

            # move_counts.append(move_counter)

end = time()

print('Played %i games' % total_games)
print('Took %.1f seconds' % (end - start))
print('Won %i games' % won_games)
print('Total win percentage: %.1f%%' % (100 * won_games / total_games))

# print('Printing expected win percentage for first ten moves')
