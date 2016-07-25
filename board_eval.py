

# set of functions to evaluate the board

# helper functions  ###########################################

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
    return(output)

# thinking functions ###########################################

def find_bombs(prob_mines, b):
    """
    Return updated probability matrix.
    Search for places that *are* mines
    """
    for i in range(b.rows):
        for j in range(b.cols):
            label = b.reveal(i, j)
            if label in range(1, 9):
                # there are bombs around
                neighbors = pull_neighbors(i, j, b)

                unknowns_neighbors = bomb_neighbors = 0

                for n in neighbors:
                    if n['label'] == b.unknown_icon:
                        unknowns_neighbors += 1
                    elif prob_mines[n['i']][n['j']] == 1:
                        bomb_neighbors += 1

                if label == bomb_neighbors:
                    # unknown neighbors are safe
                    for n in neighbors:
                        if n['label'] == b.unknown_icon:
                            prob_mines[n['i']][n['j']] = 0                    


def find_safe(prob_mines, b):
    """
    Return updated probability matrix.
    Search for places that *are not* mines
    """
    pass

def stochastic_find_safe(prob_mines, b):
    """try to find safe places when non-obvious"""
    pass
