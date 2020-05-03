import sys

from monads.either import Right, Left, Either
from monads.task import Task
from monads.list import List
from toolz import curry

# Either helpers

def fromNullable(x) -> (Either, None, 'x'):
    return Left(None) if x is None else Right(x)


def fromNullableTag(tag, x) -> (Either, str, 'x'):
    return Left(tag) if x is None else Right(x)


def fromNullableField(x, field='') -> (Either, str, 'x'):
    return Left(f'field {field} not found') if x is None else Right(x)


@curry
def prop(field, jsonDict):
    """
    f :: Dict, str -> Either[str Error, a]
    """
    res = jsonDict.get(field, None)
    return Left(f'field {field} not found') if res is None else Right(res)


@curry
def propT(jsonDict, field):
    """
    f :: Dict, str -> Either[str Error, a]
    """
    res = jsonDict.get(field, None)
    return Left(f'field {field} not found') if res is None else Right(res)


def tryCatch(f) -> (Either, str, 'x'):
    try:
        return Right(f())
    except:
        e = sys.exc_info()[0]
        return Left("Error: %s" % e)


def tryCatchTag(tag, f):
    try:
        return Right(f())
    except:
        e = sys.exc_info()[0]
        return Left(tag + "\nDetails: %s" % e)


# Natural transformations


def trace(x):
    print(x)
    return x


def eitherToTask(e: Either):
    return e.fold(Task.rejected, Task.of)


def listToDict(lstA):
    """
    f :: List a -> List B -> Dict (a, b)
    """
    return lambda lstB: dict(zip(lstA, lstB))


def zipList(lstA, lstB):
    """
    f :: List a, List b -> List (a, b)
    """
    return List(*list(zip(lstA, lstB)))


def destructure(argsNames, fn):
    return lambda args: fn(**(listToDict(argsNames)(args)))
