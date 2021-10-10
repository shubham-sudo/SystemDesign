class Snake:
    def __init__(self, head: int, tail: int) -> None:
        self._head = head
        self._tail = tail

    @property
    def head(self):
        return self._head

    @property
    def tail(self):
        return self._tail
