from typing import Iterable
from numba import njit, errors
from warnings import filterwarnings
filterwarnings("ignore", category=errors.NumbaWarning)
def optimize(f):
    try:
        return njit(f)
    except:
        return f




T = int

class PrimeSystem():

    def __init__(self, reset_state : Iterable[T]) -> None:
        self.__reset_state = list(reset_state)
        self.__primes = self.__reset_state.copy()

    def reset(self):
        self.__primes.clear()
        self.__primes.extend(self.__reset_state)

    @staticmethod
    @optimize
    def __fill(primes : list[int], n : T):
        k = primes[-1]
        while primes[-1] < n:
            k += 2
            r = k ** 0.5
            for p in primes:
                if p > r:
                    primes.append(k)
                    break
                if k % p == 0:
                    break
        
    def fill(self, n : int):
        self.__fill(self.__primes, n)

    @staticmethod
    @optimize
    def __factors(primes : list[int], n : int) -> list[int]:
        if n <= 0:
            raise ValueError("Cannot factor negative numbers yet.")
        fac = []
        for i, p in enumerate(primes):
            while n % p == 0:
                fac.append(p)
                n //= p
            if i == len(primes) - 1 and p < n ** 0.5:
                k = p
                ok = False
                while not ok:
                    k += 2
                    r = k ** 0.5
                    for p in primes:
                        if p > r:
                            primes.append(k)
                            ok = True
                            break
                        if k % p == 0:
                            break
        if n > 1:
            fac.append(n)
        return fac
    
    def factors(self, n : int):
        return self.__factors(self.__primes, n)
    
    def is_prime(self, n : int):
        return self.__factors(self.__primes, n) == [n]
    
    def is_probably_prime(self, n : int, prob : float = 0.999999) -> bool:
        if n in (2, 3):
            return True
        if n % 2 == 0:
            return False
        from random import randrange

        uncertainty = 1
        tested : set[int] = set()
        d = n - 1
        s = 0
        while d % 2 == 0:
            d //= 2
            s += 1

        a = randrange(2, n - 1)
        y = 1
        assert n - 1 == 2 ** s * d, "You failed initialization"
        while uncertainty > 1 - prob:
            while a in tested:
                a = randrange(2, n - 1)
            tested.add(a)
            x = pow(a, d, n)
            if x != 1:
                for _ in range(s):
                    if x == n - 1:
                        break
                    x = pow(x, 2, n)
                else:
                    return False
            uncertainty /= 4

        return True


def prod(s : Iterable[int]) -> int:
    p = 1
    for f in s:
        p *= f
    return p


primes = PrimeSystem((2, 3))


del Iterable