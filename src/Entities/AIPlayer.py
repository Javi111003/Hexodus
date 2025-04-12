from src.Entities.Player import Player
from src.Utils.Utils import *
from src.Utils.Algorithms.A_star import a_star_hex

# Player who chooses his moves with minimax + alpha-beta + a_star(cost_min_path) + safe_bridges
class AIPlayer(Player):

    def __init__(self, player_id: int):
        super().__init__(player_id)
        self.plays_count = 0
        self.my_safe_bridges = 0
        self.opp_safe_bridges = 0

    def play(self, board: HexBoard) -> tuple:
        n = board.size
        depth = 2 if n < 20 else 1
        bridges = n // 2 < self.plays_count or n < 19
        if self.plays_count < 1:
            self.plays_count += 1
            return get_opening_moves(board)
        if bridges:
            self.my_safe_bridges = count_safe_bridges(board, self.player_id)
            self.opp_safe_bridges = count_safe_bridges(board, 3 - self.player_id)
        row,col = self.minimax_best_move(board ,depth ,bridges)
        self.plays_count += 1
        return row,col

    def minimax(self, board: HexBoard, depth: int, maximizing_player: bool , alpha = -float('inf'), beta = float('inf'), bridges = False) -> float:
        if board.check_connection(self.player_id):
            return 1000 + 10 * depth if not maximizing_player else -1000 + 10 * depth
        if board.check_connection(3 - self.player_id):
            return -1000 + 10 * depth if maximizing_player else 1000 + 10 * depth
        if depth == 0:
            return self.eval_func(board, self.player_id)

        if maximizing_player:
            max_eval = -float('inf')
            for i , j in get_relevant_moves(board,player_id=self.player_id, bridges=bridges):
                board.place_piece(i,j, self.player_id)
                self.plays_count+=1
                new_bridges = count_bridges_around(board, self.player_id, i, j)
                self.my_safe_bridges += new_bridges
                value = self.minimax(board, depth - 1,False, alpha, beta, bridges)
                remove_piece(board, i, j, self.player_id)
                self.my_safe_bridges -= new_bridges
                self.plays_count-=1
                max_eval = max(max_eval, value)
                alpha = max(alpha, value)
                if beta <= alpha:
                    break
            return max_eval
        else:
            min_eval = float('inf')
            for i , j in get_relevant_moves(board,player_id=self.player_id, bridges=bridges):
                board.place_piece(i,j, 3 - self.player_id)
                self.plays_count+=1
                new_bridges = count_bridges_around(board,3 - self.player_id, i, j)
                self.opp_safe_bridges += new_bridges
                value = self.minimax(board, depth - 1,True, alpha, beta, bridges)
                self.plays_count-=1
                remove_piece(board, i, j, 3 - self.player_id)
                self.opp_safe_bridges -= new_bridges
                min_eval = min(min_eval, value)
                beta = min(beta, value)
                if beta <= alpha:
                    break
            return min_eval

    def minimax_best_move(self, board: HexBoard, depth: int, bridges=False):
        best_value = -float('inf')
        best_movement = None
        for row,col in get_relevant_moves(board,player_id=self.player_id,bridges=True):
            board.place_piece(row, col, self.player_id)
            new_bridges = count_bridges_around(board,self.player_id,row,col)
            self.my_safe_bridges += new_bridges
            value = self.minimax(board, depth - 1, False, best_value, float('inf'),bridges)
            remove_piece(board, row, col, self.player_id)
            self.my_safe_bridges -= new_bridges
            if value > best_value:
                best_value = value
                best_movement = (row,col)
        return best_movement

    # Eval function to estimate state cost
    def eval_func(self, board: HexBoard, player_id: int) -> float:
        w1 = 0.8  # Goal proximity (minimum cost to reach target state)
        w2 = 0.3  # Virtual connections
        w3 = 0.2 # Stones count
        cost_min_path_opp = a_star_hex(board, 3 - player_id)
        cost_min_path_player = a_star_hex(board, player_id)
        f1 = cost_min_path_opp - cost_min_path_player if cost_min_path_opp is not float('inf') else -1000
        f2 = self.my_safe_bridges - self.opp_safe_bridges
        f3 = len(board.player_positions[3 - self.player_id]) - self.plays_count
        return w1 * f1 + w2 * f2 + w3 * f3