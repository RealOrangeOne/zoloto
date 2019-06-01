import numpy


def numpy_to_py(n):
    if not isinstance(n, numpy.ndarray):
        yield float(n)
    return (numpy_to_py(item) for item in n)
