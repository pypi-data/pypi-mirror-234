from typing import Tuple, List

eps = 1e-8

class Math(object):
    def __init__(self):
        ...
    
    @classmethod
    def n_fib(cls, n: int) -> int:
        '''https://stackoverflow.com/questions/4935957/fibonacci-numbers-with-an-one-liner-in-python-3'''
        return pow(2 << n, n + 1, (4 << 2 * n) - (2 << n) - 1) % (2 << n)

    @classmethod
    def fibs(cls, n: int) -> List[int]:
        return list(map(cls.n_fib, range(1, n + 1)))

    @classmethod
    def cosine_similarity(cls, vec1: List[int], vec2: List[int]) -> float:
        import numpy as np
        array1 = np.array(vec1)
        array2 = np.array(vec2)
        return np.dot(array1, array2) / (
            np.linalg.norm(array1) * np.linalg.norm(array2) + 1e-8)

    @classmethod
    def pearson(cls, x: List[float], y: List[float]) -> float:
        import numpy as np
        return np.corrcoef(x, y)[0, 1]
    
    @classmethod
    def spearman(cls, x: List[float], y: List[float]) -> float:
        from scipy.stats import spearmanr
        return spearmanr(x, y)[0]

def spearman_correlation(vec1: List[int], vec2: List[int]) -> float:
    """https://zh.wikipedia.org/wiki/%E6%96%AF%E7%9A%AE%E5%B0%94%E6%9B%BC%E7%AD%89%E7%BA%A7%E7%9B%B8%E5%85%B3%E7%B3%BB%E6%95%B0
    """
    order_y = {i: rank + 1 for rank, i in enumerate(sorted(vec2))}
    tuples = sorted(zip(vec1, vec2), key=lambda x: x[0])
    xsum = 0
    for i, (_, y) in enumerate(tuples):
        xsum += (i + 1 - order_y[y]) ** 2
    n = len(vec1)
    return 1 - 6 * xsum / (n * (n ** 2 - 1))

if __name__ == '__main__':
    list1 = [106, 86, 100, 101, 99, 103, 97, 113, 112, 110]
    list2 = [7, 0, 27, 50, 28, 29, 20, 12, 6, 17]
    print(spearman_correlation(list1, list2))
