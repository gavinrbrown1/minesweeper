#!/usr/bin/python3

# minesweeper player, takes in a board and revealed positions and
#   outputs a choice based on lowest probability of bomb-ness

import random
from time import sleep

from board import Board

def initialize_prob_mines(b):
    """return uniform probability estimate"""
    p = mines / (rows * cols)
    prob_mines = []
    for i in range(b.rows):
         prob_mines.append([])
         for j in range(b.cols):
             prob_mines[i].append(p)
    return(prob_mines)

# temporary, only returns safe moves
def player_moves(prob_mines, b):
    """return list of moves with lowest bomb probability"""
    min_p = 0   # TEMPORARY
    # min_p = 1 # actual
    moves = []

    for i in range(b.rows):
        for j in range(b.cols):
            if b.reveal(i, j) == b.unknown_icon:
                p = prob_mines[i][j]
                if p < min_p and p != -1:
                    moves = [[i,j]]
                    min_p = p
                elif p == min_p:
                    moves.append([i, j])

    return(moves)

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
    # note that flagged mines are "officially" still unknown
    try:
        p_base = (b.mines - b.flagged) / (b.unknowns - b.flagged)
    except ZeroDivisionError:
        print('Win')
        return

    for i in range(b.rows):
        for j in range(b.cols):
            if prob_mines[i][j] not in [0, 1]:
                label = b.reveal(i, j)
                if label == b.empty_icon:
                    prob_mines[i][j] = 0
                elif label in range(10):
                    prob_mines[i][j] = 0
                elif label == b.unknown_icon:
                    prob_mines[i][j] = p_base

    return(prob_mines)

def bomb_finder(prob_mines, b):
    """search for situations where we know p is 1 or 0"""
    changed = False     # track if modifications were made
    original_prob_mines = prob_mines

    for i in range(b.rows):
        for j in range(b.cols):
            label = b.reveal(i, j)
            if label in list(range(1, 9)):
                # then there are  bomb neighbors
                neighbors = pull_neighbors(i, j, b) # list of neighboring spaces

                unknown_neighbors = bomb_neighbors = 0
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
                elif (label - bomb_neighbors) == unknown_neighbors:
                    # then all the unknown neighbors are bombs!
                    for n in neighbors:
                        if n['label'] == b.unknown_icon:
                            prob_mines[n['i']][n['j']] = 1

    for i in range(b.rows):
        for j in range(b.cols):
            if original_prob_mines[i][j] != prob_mines[i][j]:
                changed = True

    if changed:
        prob_mines = bomb_finder(prob_mines, b)

    return prob_mines

def print_probs(prob_mines):
    for row in prob_mines:
        for p in row:
            print('%0.2f' % p, end=' ')
        print()
    print()

rows = 8
cols = rows
mines = 10

lag = 2     # seconds after printing

my_board = Board(rows, cols, mines)

prob_mines = initialize_prob_mines(my_board)

# first move
my_board.move(3, 3)
prob_mines[3][3] = 0

print(my_board)

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
    print('starting to make moves')
    sleep(lag)

    moves = player_moves(prob_mines, my_board)

    print('%i safe move(s) exist(s)' % len(moves))
    sleep(lag)

    if not moves:
        break

    for [i, j] in moves:
        my_board.move(i, j)
        print(my_board)
        sleep(lag)
