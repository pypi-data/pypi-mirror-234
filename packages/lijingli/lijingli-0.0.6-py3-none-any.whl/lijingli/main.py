import numpy
from minepy import MINE

def mic(x, y):
    mine = MINE(alpha=0.6, c=15)
    mine.compute_score(x, y)
    return (mine.mic())