from src.Entities.HexBoard import HexBoard

class HexGame:
    def __init__(self, size=11, board = None):
        self.size = size
        self.hex_board = HexBoard(size) if not board else board
        self.current_player_id = 1  # R (Rojo) o A (Azul)
        self.game_over = False
        self.winner = None
        self.colors = {0: "⬜",1: "🟥", 2: "🟦"}
        self.opponents = {1: 2,2: 1}

    def print_board(self):
        """Imprime el tablero en la consola"""
        print("\n   " + " ".join(f"{i:2}" for i in range(self.size)))
        for i in range(self.size):
            print(f"{i:2} " + "  " * i, end="")
            for j in range(self.size):
                cell = self.colors[self.hex_board.board[i][j]]
                print(f" {cell} ", end="")
            print()

    def make_move(self, row, col):
        """Realiza un movimiento en el tablero"""
        if not (0 <= row < self.size and 0 <= col < self.size):
            return False, "Posición fuera del tablero"

        if self.hex_board.board[row][col] != 0:
            return False, "Casilla ya ocupada"

        self.hex_board.board[row][col] = self.current_player_id
        self.hex_board.player_positions[self.current_player_id].add((row,col))
        if self.check_winner(row, col):
            self.game_over = True
            self.winner = self.current_player_id
            return True, f"¡Jugador {self.current_player_id} gana!"

        self.current_player_id = self.opponents[self.current_player_id]
        return True, None

    def check_winner(self, row, col):
        """Verifica si el último movimiento resultó en victoria"""
        player = self.hex_board.board[row][col]
        visited = set()

        # Para R (Rojo) debe conectar izquierda (col=0) con derecha (col=size-1)
        if player == 1:
            left_edge = any(self.hex_board.board[i][0] == 1 for i in range(self.size))
            right_edge = any(self.hex_board.board[i][-1] == 1 for i in range(self.size))
            if not (left_edge and right_edge):
                return False
            return self._check_connection(row, col, player, 1)

        # Para A (Azul) debe conectar arriba (row=0) con abajo (row=size-1)
        else:
            top_edge = any(self.hex_board.board[0][j] == 2 for j in range(self.size))
            bottom_edge = any(self.hex_board.board[-1][j] == 2 for j in range(self.size))
            if not (top_edge and bottom_edge):
                return False
            return self._check_connection(row, col, player, 2)

    def _check_connection(self, row, col, player, side):
        """Usa DFS para verificar conexión entre lados opuestos"""
        stack = [(row, col)]
        visited = set()
        left_right_reached = False
        top_bottom_reached = False

        while stack:
            r, c = stack.pop()
            if (r, c) in visited:
                continue
            visited.add((r, c))

            # Verificar conexión para R (Rojo)
            if player == 1:
                if c == 0:
                    left_right_reached = True
                if c == self.size - 1:
                    top_bottom_reached = True

            # Verificar conexión para A (Azul)
            else:
                if r == 0:
                    left_right_reached = True
                if r == self.size - 1:
                    top_bottom_reached = True

            if left_right_reached and top_bottom_reached:
                return True

            # Explorar vecinos (6 direcciones en Hex)
            for dr, dc in [(-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0)]:
                nr, nc = r + dr, c + dc
                if 0 <= nr < self.size and 0 <= nc < self.size:
                    if self.hex_board.board[nr][nc] == player and (nr, nc) not in visited:
                        stack.append((nr, nc))

        return left_right_reached and top_bottom_reached
