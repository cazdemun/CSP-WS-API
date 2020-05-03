from sys import path
path.append('.')
##
from monads.task import Task
from pymonad import Right, Left, Either


"""
fold() functions are implemented for Right and Left
https://stackoverflow.com/questions/9865455/adding-functions-from-other-files-to-a-python-class
"""

Right.fold = lambda self, f, g: g(self.value)

Left.fold = lambda self, f, g: f(self.value)


# 25. Apply Natural Transformations in everyday work
print("\n25. Apply Natural Transformations in everyday work\n")


def fake(id: int):
    return ({"id": id, "name": 'user1', "best_friend_id": id + 1})


class Db:
    @staticmethod
    def find(id: int):
        return Task(lambda rej, res:
                    res(Right(fake(id)) if id > 2 else Left('not found')))


def eitherToTask(e: Either):
    return e.fold(Task.rejected, Task.of)


"""Task(Right(user))"""
Db.find(3) \
    .bind(eitherToTask) \
    .bind(lambda user: Db.find(user['best_friend_id'])) \
    .bind(eitherToTask) \
    .fork(lambda e: print(e),
          lambda u: print(u))

Db.find(1) \
    .bind(eitherToTask) \
    .bind(lambda user: Db.find(user.best_friend_id)) \
    .bind(eitherToTask) \
    .fork(lambda e: print(e),
          lambda u: print(u))
