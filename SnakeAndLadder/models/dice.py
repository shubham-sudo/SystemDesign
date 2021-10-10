from random import randint


class Dice:
    def __init__(self, min_val: int, max_val: int) -> None:
        self._min_val = min_val
        self._max_val = max_val

    @property
    def min_val(self):
        return self._min_val

    @property
    def max_val(self):
        return self._max_val

    def roll(self):
        return randint(self._min_val, self._max_val + 1)
