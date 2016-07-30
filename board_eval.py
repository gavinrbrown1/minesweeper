

# set of functions to evaluate the board

def done(b):
    for i in range(b.rows):
        for j in range(b.cols):
            if b.reveal(i,j) == b.unknown_icon:
                return(False)
    return(True)

class ProbMines():

     def __init__(self, board):
         self.probs = []
         self.rows = board.rows
         self.cols = board.cols

         p = board.mines / (self.rows * self.cols)

         for i in range(board.rows):
             self.probs.append([])
             for j in range(board.cols):
                 self.probs[i].append(p)

     def __str__(self):
         for row in self.probs:
             for p in row:
                 print('%0.2f' % p, end=' ')
             print()
         return('')

     def set(self, i, j, p):
         self.probs[i][j] = p

     def show(self, i, j):
         return(self.probs[i][j])
