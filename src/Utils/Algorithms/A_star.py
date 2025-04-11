import heapq

from src.Utils.Utils import neighbors
from src.Entities.HexBoard import HexBoard

def h(r,c, player_id, n):
    """Heurística clásica"""
    return n - 1 - c if player_id == 1 else n - 1 - r

def a_star_hex(board: HexBoard, player_id: int) -> float:
    """A* para encontrar el camino más corto en el tablero de Hex."""
    n = board.size
    start_cells = []
    goal = None
    if player_id == 1:
        start_cells = [(i,0) for i in range(n)]
        goal = lambda row , col : col == n - 1
    else:
        start_cells = [(0,i) for i in range(n)]
        goal = lambda row , col : row == n - 1
    g_score = [[1000] * n for _ in range(n)]
    open_set = []
    closed_set = []

    for r,c in start_cells:

        if board.board[r][c] == player_id:
            cost = 0
        elif board.board[r][c] == 0:
            cost = 1
        else:
            continue
        g_score[r][c] = cost
        f_score = g_score[r][c] + h(r,c,player_id,n)
        heapq.heappush(open_set, (f_score , cost , r , c))

    while open_set:
        f , current_cost , r , c = heapq.heappop(open_set)
        if (r,c) in closed_set:
            continue
        closed_set.append((r,c))

        if goal(r,c):
            return current_cost
        for nr,nc in neighbors((r,c),board):
            if (nr,nc) in closed_set:
                continue
            if board.board[nr][nc] == player_id:
                new_cost = current_cost
            elif board.board[nr][nc] == 0:
                new_cost = current_cost + 1
            else:
                new_cost = 999

            if new_cost < g_score[nr][nc]:
                g_score[nr][nc] = new_cost
                f_score = new_cost + h(nr, nc, player_id, n)
                heapq.heappush(open_set, (f_score, new_cost, nr, nc))
    return 1000
