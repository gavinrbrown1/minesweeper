# ok, let's figure this whole thing out

from player import pull_neighbors

# let's for now operate under the rule that we will always move
#   where we believe the probability of a bomb is lowest. Don't think
#   this is actually the same as optimizing our chances of winning, but I
#   do think it's pretty close

# want to simulate the possible moves and arrive at a probability distribution

# first let's write a function to take a board and a proposed mine allocation
#   and decide if it is possible

# side note: all possible positions are equally likely

def legal(board, locations):
    """returns True if the mine locations provided are possible"""

    for [i, j] in board.coords:
        label = board.reveal(i, j)

        if label in range(0, 9):
            bomb_count = 0

            neighbors = pull_neighbors(i, j, board, dist=1)

            for n in neighbors:
                if [n['i'], n['j']] in locations:
                    bomb_count += 1

            if label != bomb_count:
                return(False)

    return(True)

# now, it's obviously infeasbile to simulate every possible bomb distribution.
#   There are 64! / (10! * 54!) ways to distribute the bombs. It's a large
#   (although not astronomical) number, and we don't want to work with it.
# We can be thankful for two things. Firstly, that number comes down very
#   quickly as the game progresses. Secondly, we don't actually have to worry
#   about the entire board! We can divide the board up into three sections:
#       1) Discovered, either a number or empty
#       2) Edge, next to a number
#       3) Inaccessible, only next to edges and themselves
#   We only need to simulate the actual positions within the edge spaces, which
#   hugely cuts down our space. We may not always know the exact number of mines
#   in the edge space, but we should be able to put bounds on it

# Let's make a function to return the indices for spaces that are on the edge
