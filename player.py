#!/usr/bin/python3

# minesweeper player, takes in a board and revealed positions and
#   outputs a choice based on lowest probability of bomb-ness

import random
from time import sleep

from board import Board

def initialize_prob_mines(b):
    """return uniform probability estimate"""
    # p = mines / (rows * cols)
    prob_mines = []
    for i in range(b.rows):
         prob_mines.append([])
         for j in range(b.cols):
             prob_mines[i].append(0.1)
    return(prob_mines)

# temporary, only returns safe moves
def player_moves(prob_mines, b):
    """return a move with lowest bomb probability"""
    min_p = 0   # TEMPORARY
    # min_p = 1 # actual
    moves = []

    for [i, j] in b.coords:
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
    # print(i, j, b.rows, b.cols)

    deltas = [-1, 0, 1]
    output = []
    for di in deltas:
        for dj in deltas:
            # print(di, dj)
            if (di != 0) or (dj != 0):
                # print(i+di, j+dj)
                # print(i+di>=0)
                # print(i+di<b.rows)
                # print(j+dj>=0)
                # print(j+dj<b.cols)
                if i+di>=0 and i+di<b.rows and j+dj>=0 and j+dj<b.cols:

                    output.append({
                    'label': b.reveal(i+di, j+dj),
                    'i': i+di,
                    'j': j+dj
                    })
    return(output)

def uniform_updater(prob_mines, b):
    """do maintanence updates on prob_mines"""
    # assume everything we don't know about has same probability p
    total_mines = b.mines

    # count places we think are mines and unknown locations
    found_mines = 0
    unknowns = 0
    for [i, j] in b.coords:
        if prob_mines[i][j] not in [0, 1]:
            unknowns += 1
        elif prob_mines[i][j] == 1:
            found_mines += 1

    try:
        p = (total_mines - found_mines) / unknowns
    except ZeroDivisionError:
        pass


    # iterate over everything
    for [i, j] in b.coords:
        if prob_mines[i][j] not in [0, 1]:
            label = b.reveal(i, j)
            if label == b.empty_icon:
                prob_mines[i][j] = 0
            elif label in range(10):
                prob_mines[i][j] = 0
            elif label == b.unknown_icon:
                prob_mines[i][j] = p

    return(prob_mines)

def bomb_finder(prob_mines, b):
    """search for situations where we know p is 1 or 0"""

    for [i, j] in b.coords:
        label = b.reveal(i, j)
        if label in list(range(1, 9)):
            # then there are  bomb neighbors
            neighbors = pull_neighbors(i, j, b) # list of neighboring spaces

            unknown_neighbors = known_bomb_neighbors = 0

            for n in neighbors:
                p = prob_mines[n['i']][n['j']]
                if p == 1:
                    known_bomb_neighbors += 1
                elif p != 0:
                    unknown_neighbors += 1

            if (label - known_bomb_neighbors) == unknown_neighbors:
                # then all the unknown neighbors are bombs!
                for n in neighbors:
                    if prob_mines[n['i']][n['j']] != 0:
                        prob_mines[n['i']][n['j']] = 1

            elif label == known_bomb_neighbors:
                # then everything else surrounding is safe
                for n in neighbors:
                    if prob_mines[n['i']][n['j']] != 1:
                        prob_mines[n['i']][n['j']] = 0

    return(prob_mines)

def safe_spaces(prob_mines, b):
    """
    The places we know are not bombs.
    Possibly can be combined with bomb_finder - but need to debug!
    """
    for [i, j] in b.coords:
        label = b.reveal(i, j)
        if label in list(range(1, 9)):
            # then there are bomb neighbors
            neighbors = pull_neighbors(i, j, b) # list of neighboring spaces

            bomb_neighbors = 0

            for n in neighbors:
                if prob_mines[n['i']][n['j']] == 1:
                    bomb_neighbors += 1

            if label == bomb_neighbors:
                # then everything else surrounding is safe
                for n in neighbors:
                    if prob_mines[n['i']][n['j']] != 1:
                        prob_mines[n['i']][n['j']] = 0

    return prob_mines

def print_probs(prob_mines):
    for row in prob_mines:
        for p in row:
            print('%0.1f' % p, end=' ')
        print()
    print()

def prob_update(prob_mines, b):
    """wrapper for regular updates"""
    prob_mines = uniform_updater(prob_mines, b)
    prob_mines = bomb_finder(prob_mines, b)

    return(prob_mines)

def uncertain_mover(prob_mines, b):
    """select a move when not assured it's safe"""

    # for now, pick a random spot that is unknown
    options = []
    for [i, j] in b.coords:
        if b.reveal(i, j) == b.unknown_icon:
            options.append([i, j])

    try:
        [out] = random.sample(options, 1)
    except ValueError:
        # print("Error: you want to go, but the game is over!")
        return([-1, -1])

    return(out)

def move_chooser(prob_mines, b):
    """return a move for the player"""
    safe_moves = []

    for [i, j] in b.coords:
        if prob_mines[i][j] == 0 and b.reveal(i, j) == b.unknown_icon:
            safe_moves.append([i, j])

    if safe_moves:
        return(safe_moves)

    # no clear choices left
    return([uncertain_mover(prob_mines, b)])
