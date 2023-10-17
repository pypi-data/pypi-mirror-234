from gc import *
from sys import getrefcount
from time import sleep
from Boa.parallel.abc import Future
from Boa.parallel.process.primitives.process import *
from Boa.parallel.process.pool import *
from primes import *
from Viper.interactive import InteractiveInterpreter

n = 38243235433729167     # 38243235433729177 is actually prime
# results = [p.apply_async(primes.is_prime, i) for i in range(n, n + 200, 2)]

def count():
    k = n
    while True:
        yield k
        k += 2

def check_futures(l : list[Future]):
    print(f"{sum(f.is_set for f in l)} Futures have realized!")

def find_prime(p : Pool) -> int:
    for n, res in zip(count(), p.map(primes.is_prime, count())):
        if res:
            return n
    raise RuntimeError("How did this infinite generator ended???")

for i in range(200):

    print(f"Creating pool and searching for prime! Round {i}:")

    p = Pool(10)

    print(f"{find_prime(p)} is prime!")

    # print(getrefcount(p))
    # print(get_referrers(p))

    del p

    sleep(10)

#     raise NotImplementedError(
# """You need to create two locks for Viper.IOs:
#     - One to complete read/write operations in one block
#     - One for their Budgets to still let closing possible"""
# )

    # print(p.apply(primes.is_prime, n))

    # InteractiveInterpreter(globals()).interact()

# rt = p.create_remote_thread()


# rt.execute(primes.is_prime, 3824323543372916163)
# input("Press enter to exit.")