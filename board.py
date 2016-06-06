#!/usr/bin/python3

# minesweeper board

from random import sample

class Board():

    def __init__(self, rows, cols, mines):
        self.rows = rows
        self.cols = cols
        self.mines = mines
        self.revealed = []  # list of indices of revealed blocks

        # generate mine locations
        positions = [[x//rows, x%cols] for x in sample(range(rows*cols), mines)]

        # set up and distribute mines
        self.board = []
        for i in range(rows):
            self.board.append([])
            for j in range(cols):
                if [i, j] in positions:
                    self.board[i].append('X')
                else:
                    self.board[i].append('-')

        # calculate numbers for non-mine positions
        for i in range(rows):
            for j in range(cols):
                if self.board[i][j] != 'X':
                    total = 0
                    deltas = [-1, 0, 1]
                    for di in deltas:
                        for dj in deltas:
                            if i + di >= 0 and i + di < rows:
                                if j + dj >= 0 and j + dj < cols:
                                    if self.board[i+di][j+dj] == 'X':
                                        total += 1
                    self.board[i][j] = total

    def __str__(self):
        """cheating but this is easier"""
        for i in range(self.rows):
            for j in range(self.cols):
                if [i, j] in self.revealed:
                    if self.board[i][j] == 0:
                        print('.', sep=' ', end=' ')
                    else:
                        print(self.board[i][j], sep=' ', end=' ')
                else:
                    print('-', sep=' ', end=' ')
            print()
        return('')

    def move(self, i, j):
        """update the board with the selection at row, col"""
        # if the spot is a bomb or non-zero, we are done
        x = self.board[i][j]
        if x == 'X' or x > 0:
            self.revealed.append([i, j])

        # otherwise, need to reveal more spots as well
        # use a queue of all the spots we will reveal
        queue = [[i, j]]
        q = 0   # index in the queue
        deltas = [-1, 0, 1]
        while q < len(queue):
            r, c = queue[q][0], queue[q][1]
            if self.board[r][c] == 0:
                for di in deltas:
                    for dj in deltas:
                        if r + di >= 0 and r + di < self.rows:
                            if c + dj >= 0 and c + dj < self.cols:
                                if [r+di, c+dj] not in queue:
                                    queue.append([r+di, c+dj])
            q += 1
        self.revealed += queue
