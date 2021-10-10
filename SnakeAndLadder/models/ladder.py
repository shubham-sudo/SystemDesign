class Ladder:
    def __init__(self, start: int, end: int) -> None:
        self._start = start
        self._end = end

    @property
    def start(self):
        return self._start

    @property
    def end(self):
        return self._end
