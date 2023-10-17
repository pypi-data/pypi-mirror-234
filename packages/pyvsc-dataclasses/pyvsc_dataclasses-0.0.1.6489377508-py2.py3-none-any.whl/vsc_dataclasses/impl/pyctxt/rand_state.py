
class RandState(object):

    def __init__(self, seed : str):
        self._seed = seed

    def seed(self) -> str:
        raise NotImplementedError("seed")

    def randint32(self, low, high):
        return 0

    def randbits(self, v : 'ModelVal'):
        raise NotImplementedError("randbits")

    def setState(self, other : 'RandState'):
        raise NotImplementedError("setState")

    def clone(self) -> 'RandState':
        raise NotImplementedError("clone")

    def next(self) -> 'RandState':
        raise NotImplementedError("next")
