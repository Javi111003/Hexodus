from os import times_result

from src.Utils.Algorithms.A_star import a_star_hex
from src.Utils.Utils import remove_piece, count_safe_bridges, get_opening_moves, get_relevant_moves
from src.Entities.HexBoard import HexBoard

# Abstract class for player
class Player:
    def __init__(self, player_id: int):
        self.player_id = player_id  # Tu identificador (1 o 2)

    def play(self, board: HexBoard) -> tuple:
        raise NotImplementedError("¡Implementa este método!")