class HexBoard:
    def __init__(self, size: int, board = None):
        self.size = size  # Tamaño N del tablero (NxN)
        self.board = board if board else [[0] * size for _ in range(size)]  # Matriz NxN (0=vacío, 1=Jugador1, 2=Jugador2)
        self.player_positions = {1: set(), 2: set()}  # Registro de fichas por jugador

    def clone(self) -> 'HexBoard':
            """Devuelve una copia del tablero actual"""
            new_board = HexBoard(self.size)
            new_board.board = [row[:] for row in self.board]
            new_board.player_positions = {1: set(self.player_positions[1]), 2: set(self.player_positions[2])}
            return new_board

    def place_piece(self, row: int, col: int, player_id: int) -> bool:
        if self.board[row][col] != 0:
            return False
        self.board[row][col] = player_id
        self.player_positions[player_id].add((row,col))
        return True

    def get_possible_moves(self) -> list:
        """Devuelve todas las casillas vacías como tuplas (fila, columna)."""
        possible_moves = [(i, j) for i in range(self.size) for j in range(self.size) if self.board[i][j] == 0]
        return possible_moves

    def check_connection(self, player_id: int) -> bool:
        """Verifica si el jugador ha conectado sus dos lados (horizontal para 1, vertical para 2)"""
        n = self.size
        positions = self.player_positions.get(player_id, set())
        visited = set()
        stack = []
        if len(positions) < n:
            return  False
        # Según el jugador, definimos los bordes de entrada y condición de victoria
        if player_id == 1:
            # Jugador 1 conecta de izquierda a derecha (columnas)
            start = [pos for pos in positions if pos[1] == 0]
            condition = lambda fila, col: col == n - 1
        elif player_id == 2:
            # Jugador 2 conecta de arriba a abajo (filas)
            start = [pos for pos in positions if pos[0] == 0]
            condition = lambda row, col: row == n - 1
        else:
            return False  # ID inválido

        stack.extend(start)

        directions = [(-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0)]

        while stack:
            row, col = stack.pop()
            if (row, col) in visited:
                continue
            visited.add((row, col))

            if condition(row, col):
                return True

            for df, dc in directions:
                nf, nc = row + df, col + dc
                if (
                        0 <= nf < n and 0 <= nc < n and
                        (nf, nc) in positions and
                        (nf, nc) not in visited
                ):
                    stack.append((nf, nc))

        return False

