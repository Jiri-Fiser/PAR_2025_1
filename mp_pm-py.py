from multiprocessing import Pool
from zeta import *

xs = list(map(float, range(1, 10)))

print(xs)

def f(x):
    return zeta_numba(x, iterations=10_000)

with Pool() as pool:
    # Paralelní aplikace funkce f na každý prvek seznamu x
    results = list(pool.imap_unordered(f, xs))

print("Výsledky:", results)