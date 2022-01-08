# todo benchmark different approaches

# this can be hugely optimized with
# https://medium.com/analytics-vidhya/beating-numpy-performance-by-extending-python-with-c-c9b644ee2ca8
#
# But we do not want heavy dependencies like numpy or any can of
# platform-dependent native code.
from collections import Iterable, Collection


def _dot(vector_a: Collection[float], vector_b: Collection[float]) -> float:
    if len(vector_a) != len(vector_b):
        raise ValueError("Length mismatch")
    # todo use zip string from python 3.10
    return sum(a * b for a, b in zip(vector_a, vector_b))


def _sum_squares(vector: Iterable[float]) -> float:
    """Returns sum of squares of all numbers in vector.
    Same as `_dot(vector, vector)`"""
    return sum(x ** 2 for x in vector)


def cosine_similarity(a, b):
    return _dot(a, b) / ((_sum_squares(a) * _sum_squares(b)) ** .5)
