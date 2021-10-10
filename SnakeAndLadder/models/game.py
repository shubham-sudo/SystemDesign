from collections import deque
from random import randint
from typing import Deque, List, Set

from .board import Board
from .dice import Dice
from .ladder import Ladder
from .players import Player
from .snake import Snake


class Game:
    def __init__(self, number_of_ladders: int, number_of_snakes: int, board_size: int) -> None:
        self._number_of_ladders = number_of_ladders
        self._number_of_snakes = number_of_snakes
        self._players: Deque[Player] = deque()
        self._snakes: List[Snake] = list()
        self._ladders: List[Ladder] = list()
        self._board: Board = Board(board_size)
        self._dice: Dice = Dice(1, 6)
        self._init_board()

    @property
    def number_of_ladders(self):
        return self._number_of_ladders

    @property
    def number_of_snakes(self):
        return self._number_of_snakes

    @property
    def players(self):
        return self._players

    @property
    def snakes(self):
        return self._snakes

    @property
    def ladders(self):
        return self._ladders

    @property
    def board(self):
        return self._board

    @property
    def dice(self):
        return self._dice

    def _init_board(self):
        added_snakes: Set[str] = set()
        added_ladders: Set[str] = set()

        for _ in range(self.number_of_snakes):
            while True:
                snake_head = randint(self.board.start, self.board.size)
                snake_tail = randint(self.board.start, self.board.size)

                if snake_tail > snake_head:
                    continue

                if f"{snake_head},{snake_tail}" not in added_snakes:
                    self.snakes.append(Snake(snake_head, snake_tail))
                    added_snakes.add(f"{snake_head},{snake_tail}")
                    break

        for _ in range(self.number_of_ladders):
            while True:
                ladder_start = randint(self.board.start, self.board.size)
                ladder_end = randint(self.board.start, self.board.size)

                if ladder_end < ladder_start:
                    continue

                if f"{ladder_start},{ladder_end}" not in added_ladders:
                    self.ladders.append(Ladder(ladder_start, ladder_end))
                    added_ladders.add(f"{ladder_start},{ladder_end}")
                    break

    def add_player(self, player: Player):
        self.players.append(player)

    def play_game(self):

        while True:
            player = self.players.popleft()
            value = self.dice.roll()
            new_position = player.position + value

            # handling player position more than board end
            if new_position > self.board.end:
                self.players.append(player)
            else:
                player.position = self.find_position(new_position)

                if player.position == self.board.end:
                    player.won = True
                    print(f"Player: {player.name} Won.")
                else:
                    print(f"Setting {player.name.capitalize()}'s new position to {player.position}")
                    self.players.append(player)

            if len(self.players) < 2:
                break

    def find_position(self, new_position: int):
        for snake in self.snakes:
            if snake.head == new_position:
                print("Snake Bit")
                return snake.tail

        for ladder in self.ladders:
            if ladder.start == new_position:
                print("Climbed Ladder")
                return ladder.end

        return new_position
