class Board:
    def __init__(self, size: int) -> None:
        self._start = 1
        self._end = self.start + size - 1
        self._size = size

    @property
    def size(self):
        return self._size

    @property
    def start(self):
        return self._start

    @property
    def end(self):
        return self._end
