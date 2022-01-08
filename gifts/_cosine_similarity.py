# todo benchmark different approaches


def _dot(vector_a, vector_b) -> float:
    if len(vector_a) != len(vector_b):
        raise ValueError("Length mismatch")
    return sum(a * b for a, b in zip(vector_a, vector_b))


def cosine_similarity(a, b):
    return _dot(a, b) / ((_dot(a, a) * _dot(b, b)) ** .5)


