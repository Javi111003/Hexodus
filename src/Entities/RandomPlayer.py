# For Random Choices (RandomPlayer)
from random import Random
from src.Entities.HexBoard import HexBoard
from src.Entities.Player import Player

def random(board: HexBoard) -> tuple:
    """Returns a valid random position on board."""
    randomizer = Random("int")
    row, col = randomizer.choice(board.get_possible_moves())
    return row, col

# Random Player
class RandomPlayer(Player):

    def __init__(self, player_id: int):
        super().__init__(player_id)

    def play(self, board: HexBoard) -> tuple:
        """Select a valid random position on board"""
        row, col = random(board)
        return row, col