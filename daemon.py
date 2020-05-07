from emotiv.mock import Mock
# from cortex.classifier import Classifier

class State:
    def __init__(self, user, classifier, emotiv):
        self.user = user
        self.classifier = None
        self.emotiv = None

    def __str__(self):
        return f"{{ 'user': {self.user}, 'classifier': 'csp/lda', 'emotiv': 'mock|cortex'}}"


def initState():
    """
    f :: () -> State
    """
    init = State("cazdemun", "hello", "duh")
    print(init)
    return init


initState()