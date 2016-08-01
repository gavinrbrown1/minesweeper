# ok, let's figure this whole thing out

from math import factorial

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
#   (although not astronomical) number, and we don't want to work with itself.
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

def edges(board):
    """return list of undiscovered spaces next to discovered spaces"""
    edges = []

    for [i, j] in board.coords:
        if board.reveal(i, j) not in range(1, 9):
            neighbors = pull_neighbors(i, j, board)

            for n in neighbors:
                if board.reveal(n['i'], n['j']) in range(1,9):
                    edges.append([i,j])
                    break

    return(edges)


# Now like I mentioned before, I think it will be useful to bound the number of
#   mines that exist in the edges. Not sure exactly how to do this, but let's
#   save space for two functions that will return the upper and lower bounds for
#   the edge spaces. We can return (bad but correct) bounds right now.

def lower_bound(board, edges):
    """bound the number of mines in the edge spaces"""
    hi = 0

    for e in edges:
        i, j = e[0], e[1]
        neighbors = pull_neighbors(i, j, board)
        for n in neighbors:
            if n['label'] in range(0,9) and n['label'] > hi:
                hi = n['label']

    return(hi)

def upper_bound(board, edges):
    """bound the number of mines in the edge spaces"""

    count = 0

    for e in edges:
        i, j = e[0], e[1]
        neighbors = pull_neighbors(i, j, board)
        for n in neighbors:
            if n['label'] in range(1, 9):
                count += n['label']

    return(min(board.mines, count, len(edges)))

# well, now we're getting somewhere! Before we get all crazy with enumerating
#   the legal allocations, we should try to calculate how long that list'll be
#   (before we account for legality)

def count_possibilties(board):
    E = edges(board)

    lo = lower_bound(board, E)
    hi = upper_bound(board, E)

    count = 0

    n = len(E)

    for k in range(lo, hi+1):
        count += factorial(n) / (factorial(k) * factorial(n - k))

    return(count)

# ok, before we get into the sampling and probabilistic stuff, let's try one
#   more thing to check definitively
# want to rule out any spaces we can, answer: is is possible there is a
#   bomb at this location? All we need to do is produce one legal position with
#   a bomb at edge [i, j], which may or may not be difficult.

# let's do this.
def any_legal(i, j, E, board):
    """returns True if there is a legal position with a bomb at that location"""

    # base cases
    if [i, j] not in E:
        return(True)
    if board.reveal(i, j) == board.flag_icon:
        return(True)
    if board.reveal(i, j) != board.unknown_icon:
        return(False)

    # subset the edges; only keep edges that might influence the space in
    #   question


    return(False)


def keep_revelant(i, j, E, board):
    """
    Return list of edges that may interact with the specified edge i, j.
    Note: [i, j] not in returned list.
    """
    pass
