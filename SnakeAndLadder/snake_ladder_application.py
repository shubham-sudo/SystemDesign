from models.game import Game
from models.players import Player


class SnakeLadderApplicaion:
    @staticmethod
    def main():
        board_size = int(input("Enter Board Size: "))
        number_of_players = int(input("Enter Number of players: "))
        num_snakes = int(input("Enter number of snakes: "))
        num_ladders = int(input("Enter number of ladders: "))

        game = Game(num_ladders, num_snakes, board_size)

        for _ in range(number_of_players):
            name = input("Enter player name: ")
            game.add_player(Player(name))

        game.play_game()


if __name__ == "__main__":
    SnakeLadderApplicaion.main()
