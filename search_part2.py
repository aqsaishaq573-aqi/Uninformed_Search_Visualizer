from collections import deque
from search_part1 import get_neighbors, reconstruct_path


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
