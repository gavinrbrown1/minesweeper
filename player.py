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

def pull_neighbors(i, j, b, dist=1):
    """function returns a list of neighbors values and their indices"""
    # print(i, j, b.rows, b.cols)

    deltas = range(-dist, dist+1)
    output = []
    for di in deltas:
        for dj in deltas:
            if (di != 0) or (dj != 0):
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
        p = 0

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

    changed = False

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
                    if prob_mines[n['i']][n['j']] not in [0, 1]:
                        prob_mines[n['i']][n['j']] = 1
                        changed = True

            elif label == known_bomb_neighbors:
                # then everything else surrounding is safe
                for n in neighbors:
                    if prob_mines[n['i']][n['j']] not in [0, 1]:
                        prob_mines[n['i']][n['j']] = 0
                        changed = True

    if changed:
        prob_mines = bomb_finder(prob_mines, b)

    return(prob_mines)

def print_probs(prob_mines):
    for row in prob_mines:
        for p in row:
            print('%0.2f' % p, end=' ')
        print()
    print()

def prob_update(prob_mines, b):
    """wrapper for regular updates"""
    prob_mines = uniform_updater(prob_mines, b)

    original = [x for x in prob_mines]

    prob_mines = bomb_finder(prob_mines, b)


    if original == prob_mines:  # no 100% certainties found
        prob_mines = simple_prob_calculations(prob_mines, b)

    return(prob_mines)

def simple_prob_calculations(prob_mines, b):
    """update probabilities if no revealed spaces are interacting"""
    interaction = False
    mines_tracked = 0   # counts mines near revealed spaces
    revealed_spaces = 0

    # first, check for interactions anywhere on the board
    for [i, j] in b.coords:

        neighbors = pull_neighbors(i, j, b, dist=2)

        label = b.reveal(i, j)

        if label in range(1, 9):
            mines_tracked += label
            revealed_spaces += 1
            neighbor_spaces = len(pull_neighbors(i, j, b, dist=1))

            for n in neighbors:
                if b.reveal(n['i'], n['j']) != b.unknown_icon:
                    interaction = True
                    break

    if interaction:
        return(prob_mines)

    # if no interactions, assign exact probabilities
    untracked_mines = b.mines - mines_tracked
    non_neighbor_spaces = b.rows * b.cols - neighbor_spaces - revealed_spaces
    p_base = untracked_mines / non_neighbor_spaces

    for [i, j] in b.coords:
        if prob_mines[i][j] not in [0, 1]:
            prob_mines[i][j] = p_base

    for [i, j] in b.coords:
        label = b.reveal(i, j)
        if label in range(1, 9):
            neighbors = pull_neighbors(i, j, b)
            n_count = len(neighbors)
            for n in neighbors:
                prob_mines[n['i']][n['j']] = label / n_count

    return(prob_mines)


def uncertain_mover(prob_mines, b):
    """select a move when not assured it's safe"""

    # determine the minimum probability on the board
    lo = 1
    for [i, j] in b.coords:
        p = prob_mines[i][j]
        if p > 0 and p < lo:
            lo = p

    # for now, pick an unknown random spot with lowest mine probability
    options = []
    for [i, j] in b.coords:
        if b.reveal(i, j) == b.unknown_icon and prob_mines[i][j] == p:
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
