import abc as abc
import efg.hij as hij
from something import something

def f1(self, x, y):
    return min(x, x+y)

class C:
    f = f1

    def g(self):
        return 'hello world'
    h = g