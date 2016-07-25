

# set of functions to evaluate the board

def done(b):
    for i in range(b.rows):
        for j in range(b.cols):
            if b.reveal(i,j) == b.unknown_icon:
                return(False)
    return(True)
