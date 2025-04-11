from random import Random, random
from src.Entities.HexBoard import HexBoard

def remove_piece(board: HexBoard, row: int , col: int , player_id: int):
    board.board[row][col] = 0
    board.player_positions[player_id].remove((row, col))

def is_valid_move(row, col, n):
    return 0 <= row < n and 0 <= col < n

# Fast selections
# All relevant moves around both stones
def get_relevant_moves(board: HexBoard, player_id, bridges : bool = False) -> set:
    potential_bridges = set()
    if bridges:
        potential_bridges = get_potential_bridges(board, player_id)
    my_neighbors = get_my_filtered_neighbors(board, player_id,lambda v : v == 0)
    opp_neighbors = get_my_filtered_neighbors(board,3 - player_id,lambda v : v == 0)
    return potential_bridges.union(my_neighbors.union(opp_neighbors))

# Empty cells around player stones
def get_my_empty_neighbors(board: HexBoard, player_id: int) -> set:
    return get_my_filtered_neighbors(board, player_id)
# Function to filter player stones neighbors
def get_my_filtered_neighbors(board: HexBoard, player_id: int , predicate = lambda v : v == 0) -> set:
    result = set()
    positions = board.player_positions[player_id]
    for r , c in positions:
        for i , j in neighbors((r,c),board):
             if predicate(board.board[i][j]):
                result.add((i,j))
    return result
def get_potential_bridges(board: HexBoard, player_id: int) -> set:
    result = set()
    positions = board.player_positions[player_id]
    for i,j in positions:
        result = result.union(bridge_neighbors(i,j, board))
    return result

# Pro State Evaluation
def count_safe_bridges(board: HexBoard, player_id): # OPTIMIZAR
    c = 0
    positions = board.player_positions[player_id]
    for i,j in positions:
        for r,c in positions:
            if is_safe_bridge(i,j, r,c, board ):
                c+=1
    return c

def intersect(set_a: set,set_b: set) -> set:
    result = set()
    for a in set_a:
        if a in set_b:
            result.add(a)
    return result

def count_bridges_around(board: HexBoard, player_id, row, col) -> int:
    possible_bridges = [is_safe_bridge(row,col,i,j,board) for i,j in board.player_positions[player_id]]
    return sum([1 for cond in possible_bridges if cond])

def is_safe_bridge(x1,y1,x2,y2 ,board: HexBoard) -> bool: # OPTIMIZAR
    fst_pos_neighbors = neighbors((x1, y1), board)
    snd_pos_neighbors = neighbors((x2, y2), board)
    safe_cond = (x1,y1) != (x2,y2) and (x1,y1) not in snd_pos_neighbors and (x2,y2) not in fst_pos_neighbors
    safe_cond = safe_cond and len([(i, j) for i, j in intersect(fst_pos_neighbors, snd_pos_neighbors)
                         if board.board[i][j] == 0]) == 2
    return safe_cond

def get_opening_moves(board: HexBoard) -> tuple:
    n = board.size
    middle = n // 2
    if board.board[middle][middle] == 0:
        return middle,middle
    else:
        randomizer = Random()
        return randomizer.choice(list(neighbors((middle,middle),board)))

def neighbors(v: tuple, board: HexBoard) -> set:
    result = set()
    directions = [(-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0)]
    row, col = v
    for i, j in directions:
        nf, nc = row + i, col + j
        if is_valid_move(nf, nc, board.size):
            result.add((nf, nc))
    return result

def bridge_neighbors(row, col, board: HexBoard) -> set:
    result = set()
    directions = [(-1,-1),(-2,1),(2,-1),(-1,2),(1,-2),(1,1)]
    for i,j in directions:
        nf , nc = row + i , col + j
        if is_valid_move(nf, nc, board.size) and board.board[row][col] == 0:
            result.add((nf,nc))
    return result

def broke_bridge(i,j,player_id,board: HexBoard) -> (int,int):
    pass
