import time
import tracemalloc
from collections import deque
import heapq

#Calcule la distance de Manhattan entre deux points a=(y1,x1) et b=(y2,x2)
def heuristic(a,b):
    return abs(a[0]-b[0])+abs(a[1]-b[1])

# Directions possibles (haut, bas, gauche, droite)
directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

#Retourne les voisins accessibles d'un nœud dans le labyrinthe.
def get_neighbors(node, maze):
    x, y = node
    neighbors = []
    for dx, dy in directions:
        nx, ny = x + dx, y + dy
        # Vérifie si la case est libre
        if (nx, ny) in maze and maze[(nx, ny)] == 0:
                neighbors.append((nx, ny))
    return neighbors


# Algorithme A*
def a_star(start, goal, maze, heuristic):
    
    metrics = {'time': [], 'memory': []}
    tracemalloc.start()
    start_time = time.time()

    open_set = []
    heapq.heappush(open_set, (0 + heuristic(start, goal), start))
    came_from = {start: None}
    g_score = {start: 0}

    while open_set:
        _, current = heapq.heappop(open_set)
        metrics['time'].append(time.time() - start_time)
        metrics['memory'].append(tracemalloc.get_traced_memory()[1] / 1024)  # Mémoire en KB

        if current == goal:
            break

        for neighbor in get_neighbors(current, maze):
            tentative_g = g_score[current] + 1
            if neighbor not in g_score or tentative_g < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g
                f = tentative_g + heuristic(neighbor, goal)
                heapq.heappush(open_set, (f, neighbor))

    tracemalloc.stop()
    path = []
    current = goal
    while current:
        path.append(current)
        current = came_from.get(current)
    return path[::-1], metrics  # Retourne le chemin inversé et les métriques

# Algorithme glouton
def glouton(start, goal, maze, heuristic):
    metrics = {'time': [], 'memory': []}
    tracemalloc.start()
    start_time = time.time()

    open_set = []
    heapq.heappush(open_set, (heuristic(start, goal), start))
    came_from = {start: None}

    while open_set:
        _, current = heapq.heappop(open_set)
        metrics['time'].append(time.time() - start_time)
        metrics['memory'].append(tracemalloc.get_traced_memory()[1] / 1024)

        if current == goal:
            break

        for neighbor in get_neighbors(current, maze):
            if neighbor not in came_from:
                came_from[neighbor] = current
                priority = heuristic(neighbor, goal)
                heapq.heappush(open_set, (priority, neighbor))

    tracemalloc.stop()
    path = []
    current = goal
    while current:
        path.append(current)
        current = came_from.get(current)
    return path[::-1], metrics

# Algorithme BFS (parcours en largeur)
def bfs(start, goal, maze,heuristic=None):
    metrics = {'time': [], 'memory': []}
    tracemalloc.start()
    start_time = time.time()

    queue = deque([start])
    came_from = {start: None}

    while queue:
        current = queue.popleft()
        metrics['time'].append(time.time() - start_time)
        metrics['memory'].append(tracemalloc.get_traced_memory()[1] / 1024)

        if current == goal:
            break

        for neighbor in get_neighbors(current, maze):
            if neighbor not in came_from:
                came_from[neighbor] = current
                queue.append(neighbor)

    tracemalloc.stop()
    path = []
    current = goal
    while current:
        path.append(current)
        current = came_from.get(current)
    return path[::-1], metrics

# Algorithme DFS (parcours en profondeur).
def dfs(start, goal, maze,heuristic=None):
    metrics = {'time': [], 'memory': []}
    tracemalloc.start()
    start_time = time.time()

    stack = [start]
    came_from = {start: None}

    while stack:
        current = stack.pop()
        metrics['time'].append(time.time() - start_time)
        metrics['memory'].append(tracemalloc.get_traced_memory()[1] / 1024)

        if current == goal:
            break

        for neighbor in get_neighbors(current, maze):
            if neighbor not in came_from:
                came_from[neighbor] = current
                stack.append(neighbor)

    tracemalloc.stop()
    path = []
    current = goal
    while current:
        path.append(current)
        current = came_from.get(current)
    return path[::-1], metrics