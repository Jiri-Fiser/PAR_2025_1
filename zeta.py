import time

import numpy as np
import numba
from typing import Callable, Any
from functools import partial


def zeta_slow(x: float, iterations: int) -> float:
    return sum(1/(i**x) for i in range(1, iterations+1))

def zeta_normal(x: float, iterations: int) -> float:
    suma = 0
    for i in range(1, iterations+1):
        suma += 1/(i**x)
    return suma

def zeta_numpy(x: float, iterations: int) -> float:
    v = np.arange(1, iterations+1, dtype=float)
    return np.sum(1.0 / v ** x)

@numba.njit
def zeta_numba(x: float, iterations: int) -> float:
    suma = 0
    for i in range(1, iterations+1):
        suma += 1/(i**x)
    return suma


def benchmark(function: Callable[[],Any], iterations:int = 1000):
    start = time.perf_counter()
    for i in range(iterations):
        function()
    print(f"{function.func.__name__}: {time.perf_counter() - start}")


if __name__ == "__main__":
    #benchmark(partial(zeta_slow, 2.0, 50_000))
    #benchmark(partial(zeta_normal, 2.0, 50_000))
    benchmark(partial(zeta_numba, 9, 50_000))
    benchmark(partial(zeta_numpy, 9, 50_000))
