#!/usr/bin/python3

# minesweeper player, takes in a board and revealed positions and
#   outputs a choice based on lowest probability of bomb-ness

import random
from time import sleep

from board import Board

def player_move(prob_mines, board):
    """pick a move randomly from lowest probability of mines"""
    smallest = [1, 0, 0]
    foo = list(range(board.rows))
    bar = list(range(board.cols))

    random.shuffle(foo)
    random.shuffle(bar)

    for i in foo:
        for j in bar:
            if prob_mines[i][j] < smallest[0]:
                smallest = [prob_mines[i][j], i, j]

    return [i, j]

def pull_neighbors(i, j, b):
    """function returns a list of neighbors values and their indices"""
    deltas = [-1, 0, 1]
    output = []
    for di in deltas:
        for dj in deltas:
            if i+di>=0 and i+di<b.rows and j+dj>=0 and j+dj<b.rows:
                output.append({
                'value': b.reveal(i+di, j+dj),
                'i': i+di,
                'j': j+dj
                })
    return output

def bomb_finder(prob_mines, b):
    """search for situations where we know p in [0, 1]"""
    # b is board
    original_prob_mines = prob_mines

    # what is the probability for unknown spaces?
    p_base = (b.mines - b.flagged) / (b.unknowns)

    # search through all spaces
    for i in range(b.rows):
        for j in range(b.cols):
            x = b.reveal(i, j)

            # if there is a number, can't pick it
            if x in list(range(9)) or x == b.empty_icon:
                prob_mines[i][j] = -1

            if x in list(range(1, 9)):    # there be bombs about!
                # counters
                bomb_neighbors = x
                unknown_neighbors = flag_neighbors = 0

                neighbors = pull_neighbors(i, j, b)

                for n in neighbors:
                    if n['value'] == b.unknown_icon:
                        unknown_neighbors += 1
                    elif n['value'] == b.flag_icon:
                        flag_neighbors += 1

                if unknown_neighbors > 0:
                    if (bomb_neighbors - flag_neighbors) == unknown_neighbors:
                        p = 1
                    elif (bomb_neighbors - flag_neighbors) == 0:
                        p = 0
                    else:
                        p = p_base

                    for n in neighbors:
                        if n['value'] == b.unknown_icon:
                            if prob_mines[n['i']][n['j']] not in [0, 1]:
                                prob_mines[n['i']][n['j']] = p

    # recursive calls until prob_mines is stable
    # (wouldn't have thought of this before)
    if original_prob_mines != prob_mines:
        original_prob_mines = prob_mines
        prob_mines = self.bomb_finder(prob_mines, b)

    return(prob_mines)





    return prob_mines

def print_probs(prob_mines):
    for row in prob_mines:
        for p in row:
            print('%0.2f' % p, end=' ')
        print()
    print()

# prob_mines = bomb_finder(prob_mines, my_board)
#
# for i in range(my_board.rows):
#     for j in range(my_board.cols):
#         if prob_mines[i][j] == 1:
#             my_board.flag(i, j)
#
# prob_mines = bomb_finder(prob_mines, my_board)
#
# for i in range(my_board.rows):
#     for j in range(my_board.cols):
#         if prob_mines[i][j] == 1:
#             my_board.flag(i, j)
#
# print(my_board)
#
# print_probs(prob_mines)

# now, the flow of things:
#     initalize board and make first pick
#     calculate probabilities
#     while there are p=0 spots
#         while probabilities not stable
#             recalculate probabilities
#         flag everything we can
#         line up all p=0 spots
#         iterate through and pick them
#         calculate probabilities
#         find p=0 sites
#     end

rows = 20
cols = 20
mines = 10

lag = 1     # seconds after printing

my_board = Board(rows, cols, mines)

# generate uniform probabilistic view of minefield
p = mines / (rows * cols)
prob_mines = []
for i in range(rows):
     prob_mines.append([])
     for j in range(cols):
         prob_mines[i].append(p)

# pick = player_move(prob_mines, my_board)

my_board.move(3, 3)
prob_mines[3][3] = -1

print(my_board)
sleep(lag)

prob_mines = bomb_finder(prob_mines, my_board)

for i in range(my_board.rows):
    for j in range(my_board.cols):
        if prob_mines[i][j] == 1:
            my_board.flag(i, j)
            print(my_board)
            sleep(lag)

prob_mines = bomb_finder(prob_mines, my_board)

no_bombs = []
for i in range(rows):
    for j in range(cols):
        if prob_mines[i][j] == 0:
            no_bombs.append([i, j])

while no_bombs:
    new_prob_mines = bomb_finder(prob_mines, my_board)
    while new_prob_mines != prob_mines:
        prob_mines = new_prob_mines
        new_prob_mines = bomb_finder(prob_mines, my_board)
    prob_mines = new_prob_mines

    for i in range(my_board.rows):
        for j in range(my_board.cols):
            if prob_mines[i][j] == 1:
                my_board.flag(i, j)
                print(my_board)
                sleep(lag)

    for i in range(my_board.rows):
        for j in range(my_board.cols):
            if prob_mines[i][j] == 0:
                if [i, j] not in no_bombs:
                    no_bombs.append([i, j])

    for [i, j] in no_bombs:
        my_board.move(i, j)
        prob_mines[i][j] = -1
        print(my_board)
        sleep(lag)

    prob_mines = bomb_finder(prob_mines, my_board)
    no_bombs = []
    for i in range(rows):
        for j in range(cols):
            if prob_mines[i][j] == 0:
                no_bombs.append([i, j])

print(my_board)
# print_probs(prob_mines)
