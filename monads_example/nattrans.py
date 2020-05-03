from monads.utils import fromNullable, tryCatch, fromNullableField, eitherToTask, prop
from monads.task import Task
from monads.either import Either, Right
from monads.list import List

# more utils

def destructureArgs(lstA, fn):
    return lambda lstB: fn(**(listToDict(lstA)(lstB)))

def listToDict(lstA):
    return lambda lstB: dict(zip(lstA, lstB))

def save_task(userid: str= '5eada9b16d6559317acacf07', protocolid: str= '5eada98a6d6559317acacf05', movement: str ='right'):
    print(userid, protocolid, movement)
    return (userid, protocolid, movement)

request = {
  "json" : {
    "username": "cazdemun",
    "protocol": "graz",
    "movement": "right",
  }
}

username : Either = fromNullableField(request['json'].get('username', None), 'username')
protocol : Either = fromNullableField(request['json'].get('protocol', None), 'protocol')
movement : Either = fromNullableField(request['json'].get('movement', None), 'movement')

List('username', 'protocol', 'movement') \
    .fmap(propT(request['json'])) \
    .traverse(Task.of, eitherToTask)\
    .fmap(destructureArgs(['userid','protocolid','movement'], save_task)) \
    .fork(lambda e: print("err:", e), lambda c: print("success:", c))

print(List(lambda x: x + 2, lambda x: x + 3)
.amap(List(2, 3)))


print(List(lambda x: lambda y: x + y) \
.amap(List(2, 3)) \
.amap(List(5, 6)))

print(List(*list(zip(List(2,3),List(4,5)))))