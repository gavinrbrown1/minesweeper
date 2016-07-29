
# main script

from time import sleep, time

from player import initialize_prob_mines, prob_update, move_chooser
from board import Board, board_setup
from board_eval import done

# parameters ########################
verbose = True
difficulty = 'easy'     # 'hard' or 'easy'

won_games = 0
total_games = 1000

[rows, cols, mines, init_row, init_col] = board_setup(difficulty)

lag = 3  # seconds after printing

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
        # otherwise, let's play!

        # gameplay ########################
        while True:
            # initial probabilities
            prob_mines = prob_update(prob_mines, my_board)

            # start by flagging what we know to be bombs
            flagged = 0

            for [i, j] in my_board.coords:
                label = my_board.reveal(i, j)
                if prob_mines[i][j] == 1 and label != my_board.flag_icon:
                    my_board.flag(i, j)
                    flagged += 1

            if verbose and flagged > 0:
                print('Flagged %i bombs' % flagged)
                print(my_board)
                # print_probs(prob_mines)
                sleep(lag)

            # probabilties agains
            # prob_mines = prob_update(prob_mines, my_board)

            # where is safe? Move there
            # prob_mines = safe_spaces(prob_mines, my_board)

            moves = move_chooser(prob_mines, my_board)
            x = len(moves)

            lost = False

            for [i, j] in moves:
                if my_board.reveal(i, j) == my_board.unknown_icon:
                    revealed = my_board.move(i, j)
                    if verbose:
                        print('Moving')
                        print(my_board)
                        # print_probs(prob_mines)
                        sleep(lag)

                    if revealed == my_board.mine_icon:
                        lost = True
                        if x > 1:
                            print('shit')

            if lost:
                break

            if done(my_board):
                won_games += 1
                break

end = time()

print('Played %i games' % total_games)
print('Took %.1f seconds' % (end - start))
print('Won %i games' % won_games)
print('Total win percentage: %.1f%%' % (100 * won_games / total_games))

# print('Printing expected win percentage for first ten moves')
