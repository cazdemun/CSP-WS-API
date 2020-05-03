import oslash
from oslash import Just, Right, Left

print(Just(2).map(lambda x: x+3))


def findColor(name: str) -> [Right, Left]:
    # found = ({'red': '#ff4444', 'blue': '#3b5998', 'yellow': '#fff68f'})[name]
    found = (
        {'red': '#ff4444', 'blue': '#3b5998', 'yellow': '#fff68f'}
    ).get(name, None)
    return Right(found) if found else Left(None)


result = findColor('blue') \
    .map(lambda c: c[1:]) \
    .bind(lambda c: c.upper())
# .bind(lambda e: 'no color',
#       lambda c: c.upper())

result2 = findColor('green') \
    .map(lambda c: c[1:]) \
    .bind(lambda c: c.upper())

print(result)
print(result2)
print(findColor('blue'))
print(findColor('green'))
