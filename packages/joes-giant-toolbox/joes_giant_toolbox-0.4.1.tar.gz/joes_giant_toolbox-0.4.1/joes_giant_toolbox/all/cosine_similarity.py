"""This script declares the function cosine_similarity()"""

import numpy as np


def cosine_similarity(vec1: np.ndarray, vec2: np.ndarray) -> np.ndarray:
    """Calculates the cosine similarity between two 1-dimensional numpy arrays\n
    The "cosine similarity" is the cosine of the angle between the 2 vectors\n
    It is defined:
        cosine_similarity(vec1,vec2) = ( vec1 · vec2 ) / ( ||vec1|| * ||vec2|| )\n
    Parameters
    ----------
    vec1 : numpy.array
        A 1-dimensional numpy array
    vec2 : numpy.array
        A 1-dimensional numpy array (of the same shape as vec1)
    Returns
    -------
    numpy.array
    """
    return np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))
