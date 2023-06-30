import pandas
import pandas as pd
import panel
import panel as pn
import pkg.sub_pkg
import pkg.sub_pkg as name
from hij.edf import abc as xyz
from module import pkg
from module import pkg as name
from module.sub_module import pkg as name
from some_new_module.new_sub_module.constants.plots_constants2 import (
    abc,
    abc2,
    abc3,
    defg,
    defg2,
    defg3,
    hij,
    hij2,
    hij3,
)
from some_other_module.sub_module.constants.plots_constants2 import (
    abc,
    abc3,
    defg,
    defg3,
    hij,
    hij3,
    something,
    that,
    this,
)


def func():
    sum = 0
    for i in range(10):
        i += 10
    return sum


# This file is only consumed by test_aggregate.py to test the aggregation functions from the aggregate_file.py script.


def code():
    a = 1
    b = 2
    return lambda x: x + a * b


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
    print(p)
