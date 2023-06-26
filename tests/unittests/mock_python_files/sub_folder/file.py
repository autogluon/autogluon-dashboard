import itertools

def iter_primes():
     numbers = itertools.count(2)

     while True:
         prime = next(numbers)
         yield prime
         numbers = filter(prime.__rmod__, numbers)

for p in iter_primes():
    if p > 1000:
        break
    print (p)