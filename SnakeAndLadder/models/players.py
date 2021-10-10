class Player:
    def __init__(self, name: str):
        self._name: str = name
        self._position: int = 0
        self._won: bool = False

    @property
    def name(self):
        return self._name

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, value: int):
        self._position = value

    @property
    def won(self):
        return self._won

    @won.setter
    def won(self, value: bool):
        self._won = value
