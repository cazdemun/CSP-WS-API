import sys

import json
from pymonad import Right, Left, Either

"""
fold() functions are implemented for Right and Left
https://stackoverflow.com/questions/9865455/adding-functions-from-other-files-to-a-python-class
"""

Right.fold = lambda self, f, g: g(self.value)

Left.fold = lambda self, f, g: f(self.value)

# 3. Enforce a null check with composable code branching using Either
print("\n3. Enforce a null check with composable code branching using Either\n")


def fromNullable(x) -> (Either, None, 'x'):
    return Left(None) if x is None else Right(x)


def findColor(name: str) -> (Either, None, str):
    return fromNullable((
        {'red': '#ff4444', 'blue': '#3b5998', 'yellow': '#fff68f'}
    ).get(name, None))


result: str = findColor('blue') \
    .fmap(lambda c: c[1:]) \
    .fold(lambda e: 'no color',
          lambda c: c.upper())

print(result)

result: str = findColor('green') \
    .fmap(lambda c: c[1:]) \
    .fold(lambda e: 'no color',
          lambda c: c.upper())

print(result)

# 4. Use chain for composable error handling with nested Eithers
print("\n4. Use chain for composable error handling with nested Eithers\n")


def tryCatch(f) -> (Either, str, 'x'):
    try:
        return Right(f())
    except:
        e = sys.exc_info()[0]
        return Left("Error: %s" % e)


def getPort(path: str) -> int:
    return tryCatch(lambda: open(path, "r").read()) \
        .bind(lambda x: tryCatch(lambda: json.loads(x))) \
        .fold(lambda e: trace(e, 8888),
              lambda c: c['port'])


def trace(tag, x):
    print("Trace\tTag:", tag, "x:", x)
    return x


print(getPort("monads_example/config.json"))

print(getPort("monads_example/badconfig.json"))

print(getPort("monads_example/confi.json"))


# 5. A collection of Either examples compared to imperative code
print("\n5. A collection of Either examples compared to imperative code\n")

# # example 1


# def openSite():
#     if current_user is not None:
#         return renderPage(current_user)
#     else:
#         return showLogin()


# def openSite():
#     return fromNullable(curren_user) \
#         .fold(showLogin, renderPage)

# # example 2


# def getPrefs(user):
#     if user.premium:
#         return loadPrefs(user.preferences)
#     else:
#         return defaultPrefs


# def getPrefs(user):
#     return (Right(user) if user.premium else Left('not premium')) \
#         .fmap(lambda u: u.preferences) \
#         .fold(lambda e: defaultPrefs,
#               lambda prefs: loadPrefs(prefs))

# # example 3


# def streetName(user):
#     address = user.address

#     if address is not None:
#         street = address.street

#         if street is not None:
#             return street.name

#     return 'no street'


# def streeName(user):
#     return fromNullable(user.address) \
#         .bind(lambda a: fromNullable(a.street)) \
#         .fmap(lambda s: s.name) \
#         .fold(lambda e: 'no street',
#               lambda n: n)


# # example 4

# def concatUniq(x, ys):
#     found = filter(lambda y: y == x, ys)[0]
#     return ys if found else concat(ys, x)


# def concatUniq(x, ys):
#     return fromNullable(filter(lambda y: y == x, ys)[0]) \
#         .fold(lambda e: ys.concat(x), lambda y: ys)

# # example 5

# wrapExamples

# # example 6

# parseDbUrl
