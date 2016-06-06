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
            if (di != dj) or (di != 0):
                if i+di>=0 and i+di<b.rows and j+dj>=0 and j+dj<b.rows:
                    output.append({
                    'label': b.reveal(i+di, j+dj),
                    'i': i+di,
                    'j': j+dj
                    })
    return output

def basic_updater(prob_mines, b):
    """do maintanence updates on prob_mines"""
    p_base = (b.mines - b.flagged) / (b.unknowns - b.flagged)

    for i in range(b.rows):
        for j in range(b.cols):
            if prob_mines[i][j] not in [-1, 0, 1]:
                label = b.reveal(i, j)
                if label == b.empty_icon:
                    prob_mines[i][j] = -1
                elif label in range(10):
                    prob_mines[i][j] = -1
                elif label == b.unknown_icon:
                    prob_mines[i][j] = p_base

    return(prob_mines)

def bomb_finder(prob_mines, b):
    """search for situations where we know p is 1"""
    original_prob_mines = [x for x in prob_mines]

    for i in range(b.rows):
        for j in range(b.cols):
            label = b.reveal(i, j)
            if label in list(range(1, 9)):
                # then there are be bomb neighbors
                unknown_neighbors = bomb_neighbors = 0
                neighbors = pull_neighbors(i, j, b) # list of neighboring spaces
                for n in neighbors:
                    if n['label'] == b.unknown_icon:
                        unknown_neighbors += 1
                    elif prob_mines[n['i']][n['j']] == 1:
                        bomb_neighbors += 1

                if label == bomb_neighbors:
                    # then all the unknown neighbors are safe!
                    for n in neighbors:
                        if n['label'] == b.unknown_icon:
                            prob_mines[n['i']][n['j']] = 0
                elif label == unknown_neighbors:
                    # then all the unknown neighbors are bombs!
                    for n in neighbors:
                        if n['label'] == b.unknown_icon:
                            prob_mines[n['i']][n['j']] = 1

    if original_prob_mines != prob_mines:
        print('hello')
        original_prob_mines = prob_mines
        prob_mines = self.bomb_finder(original_prob_mines, b)

    return prob_mines

def no_bomb_finder(prob_mines, b):
    """search for spaces where there is no bomb"""
    pass

def print_probs(prob_mines):
    for row in prob_mines:
        for p in row:
            print('%0.2f' % p, end=' ')
        print()
    print()


rows = 8
cols = rows
mines = 10
#
lag = 2     # seconds after printing
#
my_board = Board(rows, cols, mines)
#
# generate uniform probabilistic view of minefield
p = mines / (rows * cols)
prob_mines = []
for i in range(rows):
     prob_mines.append([])
     for j in range(cols):
         prob_mines[i].append(p)
#
# # pick = player_move(prob_mines, my_board)
#
my_board.move(3, 3)
prob_mines[3][3] = -1

print(my_board)

prob_mines = basic_updater(prob_mines, my_board)
prob_mines = bomb_finder(prob_mines, my_board)


for i in range(my_board.rows):
    for j in range(my_board.cols):
        if prob_mines[i][j] == 1:
            my_board.flag(i, j)
            print(my_board)
            sleep(lag)

prob_mines = basic_updater(prob_mines, my_board)

prob_mines = bomb_finder(prob_mines, my_board)


for i in range(my_board.rows):
    for j in range(my_board.cols):
        if prob_mines[i][j] == 1:
            my_board.flag(i, j)
            print(my_board)
            sleep(lag)

# print(my_board)

print_probs(prob_mines)
