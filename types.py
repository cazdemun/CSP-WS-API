import mne

class Model:
    
    KINDS = ("CSP-LDA", "LSTM", "LSTM-RL")

    def __init__(self, kind, data=None):
        if kind not in self.KINDS:
            raise NameError("{} invalid variant!".format(kind))
        self.kind = kind
        self.data = data

class Protocol:

    KINDS = ("GRAZ", "A-BCI", "MINDRACE")

    def __init__(self, kind, conf = {"max_sessions": 6, "max_runs": 4, "max_tasks": 10, "max_movements": 3}):
        if kind not in self.KINDS:
            raise NameError("{} invalid variant!".format(kind))
        self.kind = kind
        self.conf = conf

class User:
    def __init__(self, name : str):
        self.username : str = name

class Session:
    def __init__(self, tasks):
        self.tasks : List[Task] = tasks

class Task: # enum (Left, Right, Forward) # join - not commutative group

    KINDS = ("Left, Right, Forward")

    def __init__(self, kind, duration, sps, data):
        if kind not in self.KINDS:
            raise NameError("{} invalid variant!".format(kind))
        self.kind = kind
        self.duration : float = duration
        self.sps : int = sps
        self.data : mne.Raw = data
