from pymonad import Monad
from toolz import compose

"""
Implementation adapted from: https://mostly-adequate.gitbooks.io/mostly-adequate-guide/appendix_b.html#task
And Right monad from PyMonad
"""

class Task(Monad):
    def __init__(self, fork):
        super(Task, self).__init__(fork)
        self.fork = self.value

    def __eq__(self, other):
        super(Task, self).__eq__(other)
        if not isinstance(other, Task):
            return False
        elif (self.getValue() == other.getValue()):
            return True
        else:
            return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def __str__(self):
        return "Task: " + str(self.getValue())

    def fmap(self, function):
        return Task(lambda reject, resolve: self.fork(reject, compose(resolve, function)))

    def amap(self, functorValue):
        return self.bind(lambda fn: functorValue.fmap(fn))

    def bind(self, function):
        return Task(lambda reject, resolve: self.fork(reject, lambda x: function(x).fork(reject, resolve)))

    @staticmethod
    def rejected(x):
        return Task(lambda reject, _: reject(x))

    @staticmethod
    def of(x):
        return Task(lambda _, resolve: resolve(x))
