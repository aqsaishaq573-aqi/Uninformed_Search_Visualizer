from collections import deque
import heapq

# Clockwise movement order (ALL diagonals included)
MOVES = [
    (-1, 0),   # Up
    (0, 1),    # Right
    (1, 0),    # Down
    (1, 1),    # Bottom-Right
    (0, -1),   # Left
    (-1, -1),  # Top-Left
    (-1, 1),   # Top-Right
    (1, -1)    # Bottom-Left
]


def get_neighbors(node, grid, rows, cols):
    neighbors = []
    for dr, dc in MOVES:
        r = node[0] + dr
        c = node[1] + dc
        if 0 <= r < rows and 0 <= c < cols:
            if grid[r][c] == 0:
                neighbors.append((r, c))
    return neighbors


def reconstruct_path(parent, goal):
    path = []
    while goal in parent:
        path.append(goal)
        goal = parent[goal]
    return path[::-1]


# ---------------- BFS ----------------
def bfs(start, goal, grid, rows, cols):
    queue = deque([start])
    visited = set()
    parent = {}

    while queue:
        node = queue.popleft()

        if node == goal:
            return reconstruct_path(parent, node)

        if node not in visited:
            visited.add(node)

            for neighbor in get_neighbors(node, grid, rows, cols):
                if neighbor not in visited:
                    parent[neighbor] = node
                    queue.append(neighbor)

    return []


# ---------------- DFS ----------------
def dfs(start, goal, grid, rows, cols):
    stack = [start]
    visited = set()
    parent = {}

    while stack:
        node = stack.pop()

        if node == goal:
            return reconstruct_path(parent, node)

        if node not in visited:
            visited.add(node)

            for neighbor in reversed(get_neighbors(node, grid, rows, cols)):
                if neighbor not in visited:
                    parent[neighbor] = node
                    stack.append(neighbor)

    return []


# ---------------- UCS ----------------
def ucs(start, goal, grid, rows, cols):
    pq = []
    heapq.heappush(pq, (0, start))
    parent = {}
    cost = {start: 0}

    while pq:
        current_cost, node = heapq.heappop(pq)

        if node == goal:
            return reconstruct_path(parent, node)

        for neighbor in get_neighbors(node, grid, rows, cols):
            new_cost = current_cost + 1
            if neighbor not in cost or new_cost < cost[neighbor]:
                cost[neighbor] = new_cost
                parent[neighbor] = node
                heapq.heappush(pq, (new_cost, neighbor))

    return []


# ---------------- DLS ----------------
def dls(start, goal, grid, rows, cols, limit):
    stack = [(start, 0)]
    parent = {}

    while stack:
        node, depth = stack.pop()

        if node == goal:
            return reconstruct_path(parent, node)

        if depth < limit:
            for neighbor in reversed(get_neighbors(node, grid, rows, cols)):
                parent[neighbor] = node
                stack.append((neighbor, depth + 1))

    return []


# ---------------- IDDFS ----------------
def iddfs(start, goal, grid, rows, cols):
    for depth in range(1, rows * cols):
        result = dls(start, goal, grid, rows, cols, depth)
        if result:
            return result
    return []


# ---------------- Bidirectional ----------------
def bidirectional(start, goal, grid, rows, cols):
    queue_start = deque([start])
    queue_goal = deque([goal])
    visited_start = {start}
    visited_goal = {goal}
    parent = {}

    while queue_start and queue_goal:

        node_start = queue_start.popleft()
        node_goal = queue_goal.popleft()

        if node_start in visited_goal:
            return reconstruct_path(parent, node_start)

        if node_goal in visited_start:
            return reconstruct_path(parent, node_goal)

        for neighbor in get_neighbors(node_start, grid, rows, cols):
            if neighbor not in visited_start:
                visited_start.add(neighbor)
                parent[neighbor] = node_start
                queue_start.append(neighbor)

        for neighbor in get_neighbors(node_goal, grid, rows, cols):
            if neighbor not in visited_goal:
                visited_goal.add(neighbor)
                queue_goal.append(neighbor)

    return []
