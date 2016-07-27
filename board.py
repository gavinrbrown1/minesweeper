#!/usr/bin/python3

# minesweeper board

from random import sample

def board_setup(difficulty):
    """
    Return parameters to initialize the game
    [rows, cols, mines, init_row, init_col]
    """
    if difficulty == 'hard':
        return([16, 30, 99, 7, 14])
    elif difficulty == 'easy':
        return([8, 8, 10, 3, 3])
    else:
        print('Incorrect difficulty specified, must be \'hard\' or \'easy\'')


class Board():

    def __init__(self, rows, cols, mines):
        # parameters
        self.rows = rows
        self.cols = cols
        self.mines = mines

        # symbols
        self.mine_icon = 'X'
        self.empty_icon = '.'
        self.unknown_icon = '~'
        self.flag_icon = 'F'

        # counters
        self.exploded = False
        self.flagged = 0
        self.unknowns = self.rows * self.cols

        # for iterating over coordinates
        self.coords = []

        for i in range(self.rows):
            for j in range(self.cols):
                self.coords.append([i, j])

        # generate mine locations
        positions = [[x//cols, x%cols] for x in sample(range(rows*cols), mines)]

        # each element of the board has two entries: the first is actual entry
        #   and the second is what the player sees
        # set up and distribute mines
        self.board = []
        for i in range(rows):
            self.board.append([])
            for j in range(cols):
                if [i, j] in positions:
                    self.board[i].append([self.mine_icon, self.unknown_icon])
                else:
                    self.board[i].append([self.unknown_icon, self.unknown_icon])

        # calculate numbers for non-mine positions
        for i in range(rows):
            for j in range(cols):
                if self.board[i][j][0] != self.mine_icon:
                    total = 0
                    deltas = [-1, 0, 1]
                    for di in deltas:
                        for dj in deltas:
                            if di != dj or di != 0:
                                if i+di>=0 and i+di<rows and j+dj>=0 and j+dj<cols:
                                    if self.board[i+di][j+dj][0] == self.mine_icon:
                                            total += 1
                    self.board[i][j][0] = total

    def __str__(self):
        """cheating but this is just easier"""
        for i in range(self.rows):
            for j in range(self.cols):
                if self.board[i][j][1] != '-':
                    if self.board[i][j][1] == 0:
                        print(self.empty_icon, sep=' ', end=' ')
                    else:
                        print(self.board[i][j][1], sep=' ', end=' ')
                else:
                    print(self.unknown_icon, sep=' ', end=' ')
            print()
        print('%i/%i mines remaining' % ((self.mines - self.flagged), self.mines))
        return('')

    def move(self, x, y):
        """update the board with the selection at row, col"""

        i, j = x, y

        # use a queue of all the spots we will reveal
        queue = [[i, j]]
        q = 0   # index in the queue
        deltas = [-1, 0, 1]
        while q < len(queue):
            r, c = queue[q][0], queue[q][1]
            if self.board[r][c][0] == 0:
                for di in deltas:
                    for dj in deltas:
                        if di != dj or di != 0:
                            if r+di>=0 and r+di<self.rows:
                                if c+dj>=0 and c+dj<self.cols:
                                    if [r+di, c+dj] not in queue:
                                        queue.append([r+di, c+dj])
            q += 1

        for [i, j] in queue:
            self.board[i][j][1] = self.board[i][j][0]

        self.unknowns -= len(queue)

        return(self.reveal(x, y))

    def flag(self, i, j):
        """update the board with flag"""
        self.board[i][j][1] = self.flag_icon
        self.flagged += 1

    def reveal(self, i, j):
        """what the player uses to see a single spot"""
        return self.board[i][j][1]

    def check_win(self):
        """checks end conditions"""
        if self.exploded:
            return('Lost')
        if self.flagged == self.mines and self.unknowns == 0:
            return('Won')
        else:
            return('Continue')
