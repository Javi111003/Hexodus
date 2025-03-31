import heapq

def manhattan_distance(state):
    n = len(state[0])
    distance = 0
    for i in range(n):
        for j in range(n):
            if state[i][j] == 0:
                continue
            x_target = state[i][j] // n
            y_target = state[i][j] % n
            distance += abs(i - x_target) + abs(j - y_target)
    return distance

def get_neighbors(state):
    neighbors = []
    n = len(state[0])
    row, col = next((i, j) for i in range(n) for j in range(n) if state[i][j] == 0)

    # Movimientos posibles
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    for dr, dc in directions:
        new_row, new_col = row + dr, col + dc
        if 0 <= new_row < n and 0 <= new_col < n:
            new_state = list(list(row) for row in state)
            new_state[row][col], new_state[new_row][new_col] = new_state[new_row][new_col], new_state[row][col]
            neighbors.append(tuple(tuple(r) for r in new_state))

    return neighbors


def a_star_n_puzzle(initial_state, goal_state, h = manhattan_distance,show_path=False):
    open_list = []
    heapq.heappush(open_list, (h(initial_state), 0, initial_state, None))
    explored_nodes = 1
    visited = {initial_state: (None, 0, h(initial_state))}
    while open_list:
        current = heapq.heappop(open_list)
        f_current, g_current, state_current, parent = current

        if state_current == goal_state:
            path = []
            while state_current is not None:
                path.append(state_current)
                state_current = visited[state_current][0]
            path.reverse()

            if show_path:
                print("Pasos intermedios:")
                for step in path:
                    print("\n".join(" ".join(map(str, row)) for row in step))
                    print("---")
            return len(path) - 1, explored_nodes

        if state_current in visited and g_current > visited[state_current][1]:
            continue

        for neighbor in get_neighbors(state_current):
            g_neighbor = g_current + 1
            h_neighbor = h(neighbor)
            f_neighbor = g_neighbor + h_neighbor

            if neighbor not in visited or g_neighbor < visited.get(neighbor, (None, float('inf'), None))[1]:
                visited[neighbor] = (state_current, g_neighbor, h_neighbor)
                heapq.heappush(open_list, (f_neighbor, g_neighbor, neighbor, state_current))
                explored_nodes += 1

    return -1 , -1  # No hay solución


if __name__ == "__main__":
    # A-star
    init_state = (
        (1, 2, 5),
        (3, 4, 8),
        (6, 0, 7)
    )
    target_state = (
        (0, 1, 2),
        (3, 4, 5),
        (6, 7, 8)
    )
    print("A* algorithm")
    optimal_moves = a_star_n_puzzle(init_state, target_state, manhattan_distance,show_path=True)
    print(f"Número de movimientos óptimos: {optimal_moves[0]}")
    print(f"Número de nodos explorados: {optimal_moves[1]}")
    print("-" * 15)
    # Simulando Dijkstra para comparar comportamiento
    # Contando la cantidad de expansiones que hace el arbol de búsqueda
    print("Dijkstra algorithm")
    optimal_moves = a_star_n_puzzle(init_state, target_state, lambda x: 0,show_path=False) # la función constante 0 me asegura que la función de prioridad sea: f(n) = g(n)
    print(f"Número de movimientos óptimos: {optimal_moves[0]}")
    print(f"Número de nodos explorados: {optimal_moves[1]}")