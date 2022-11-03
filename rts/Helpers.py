import numpy as np

def urm(n: int):
    return n * (np.power(2, 1/n) - 1)