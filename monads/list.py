from pymonad import List
from functools import reduce

List.traverse = lambda self, of, fn: reduce(lambda f, a: of(lambda b: lambda bs: bs + List(b)).amap(fn(a)).amap(f), self, of(List()))

List = List