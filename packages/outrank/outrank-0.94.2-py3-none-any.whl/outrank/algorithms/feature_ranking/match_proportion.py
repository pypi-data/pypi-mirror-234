from __future__ import annotations

import numpy as np
from numba import njit


@njit(
    'float32(int32[:], int32[:])',
    cache=True,
    fastmath=True,
    error_model='numpy',
    boundscheck=True,
)
def match_proportion(input_first, input_second):
    """Jaccard score - simplified"""
    intersection_count = 0
    for element in input_first:
        if element in input_second:
            intersection_count += 1
    return np.divide(intersection_count, len(input_second))


if __name__ == '__main__':
    order = 15
    a = np.random.randint(1000, size=2**(order - 1)).astype(np.int32)
    b = np.random.randint(1000, size=2**order).astype(np.int32)
    assert match_proportion(a, b) == 0.5

    a = np.random.randint(1000, size=2**(order - 2)).astype(np.int32)
    b = np.random.randint(1000, size=2**order).astype(np.int32)
    assert match_proportion(a, b) == 0.25
