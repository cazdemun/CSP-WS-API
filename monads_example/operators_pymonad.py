import json
from pymonad import Just, List

print(Just(2).fmap(lambda x: x+3))

def just_positive_and_negative(x):
    return Just(x + 3)

print(Just(lambda x: x+3) >> Just(2)) # Just 2
print(Just(2) >> Just(lambda x: x+3) >> Just(6)) # Just 6
print(Just(2) >> just_positive_and_negative) # Just 5

def positive_and_negative(x):
    return List(x, -x)

print(Just(2) >> positive_and_negative) # [2, -2]
print(List(9) >> positive_and_negative) # [9, -9]

print(Just(2).fmap(lambda x: x+3))