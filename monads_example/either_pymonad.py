import sys
import os

import json
from pymonad import Just, Right, Left

"""
The main problem with this is that we do not have the fold function.
I could actually try to implement it (clean or as a Monad), but whatever.
https://stackoverflow.com/questions/9865455/adding-functions-from-other-files-to-a-python-class

Right.fold = lambda self,f,g: g(self.value)

Left.fold = lambda self,f,g: f(self.value)

"""

# 3. Enforce a null check with composable code branching using Either
print("\n3. Enforce a null check with composable code branching using Either\n")


def fromNullable(tag: str, x) -> [Right, Left]:
    return Right(x) if x is not None else Left(tag)


def findColor(name: str) -> [Right, Left]:
    return fromNullable('no color', (
        {'red': '#ff4444', 'blue': '#3b5998', 'yellow': '#fff68f'}
    ).get(name, None))


result = findColor('blue') \
    .fmap(lambda c: c[1:]) \
    .bind(lambda c: c.upper())

print(result)

result = findColor('green') \
    .fmap(lambda c: c[1:]) \
    .bind(lambda c: c.upper())

print(result)

# 4. Use chain for composable error handling with nested Eithers
print("\n4. Use chain for composable error handling with nested Eithers\n")


def tryCatch(f):
    try:
        return Right(f())
    except:
        e = sys.exc_info()[0]
        return Left("Error: %s" % e)


def getPort(path: str) -> int:
    return tryCatch(lambda: open(path, "r").read()) \
        .bind(lambda x: tryCatch(lambda: json.loads(x))) \
        .bind(lambda c: c['port'])
    # .fold(lambda e: 3000,
    #         lambda c: c['port'])


print(getPort("monads_example/config.json"))

print(getPort("monads_example/badconfig.json"))

print(getPort("monads_example/confi.json"))
