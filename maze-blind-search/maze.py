"""creation labyrinthe"""

# Le labyrinthe est représenté sous forme de dictionnaire :
# (x, y) : "." pour une case libre, "#" pour un mur.

maze = {
    (0, 0): ".", (0, 1): "#", (0, 2): ".", (0, 3): ".",
    (1, 0): ".", (1, 1): ".", (1, 2): ".", (1, 3): "#",
    (2, 0): "#", (2, 1): ".", (2, 2): ".", (2, 3): "#",
    (3, 0): ".", (3, 1): "#", (3, 2): ".", (3, 3): "."
}

# Coordonnées de départ et d'arrivée
start = (0, 0)
goal = (3, 3) 

# Directions : Haut, Bas, Gauche, Droite
directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

# pour savoir quels sont les voisins accessibles selon la case courante 
# pour ne pas sortir du labyrinthe ,ni traverser le mur
def get_neighbors(node, maze, directions):
    neighbors = []
    for dx, dy in directions:
        neighbor = (node[0] + dx, node[1] + dy)
        if neighbor in maze and maze[neighbor] == ".":
            neighbors.append(neighbor)
    return neighbors

# Dimensions du labyrinthe
taille_x = 4
taille_y = 4

# Affichage du labyrinthe
def afficher_labyrinthe(maze, taille_x, taille_y, path=None):
    for x in range(taille_x):
        for y in range(taille_y):
            # Vérifier si la case appartient au chemin
            if path and (x, y) in path:
                print("p", end="  ")  # Marquer le chemin avec "p"
            else:
                print(maze.get((x, y), "#"), end="  ")
        print()

# Afficher le labyrinthe
print("Labyrinthe initial :\n")
afficher_labyrinthe(maze, taille_x, taille_y)

""" algorithmes pour resoudre le labyrinthe"""
from collections import deque

# Algorithme BFS (Breadth-First Search)
def bfs(start, goal, maze, directions):
    queue = deque([(start, [start])])  # File contenant la position actuelle et le chemin parcouru
    visited = set()  # Ensemble des positions déjà visitées

    while queue:
        current, path = queue.popleft()
        if current == goal:
            return path  # Retourne le chemin si le but est atteint

        if current in visited:
            continue
        visited.add(current)

        # Explorer les voisins
        for neighbor in get_neighbors(current, maze, directions):
            if neighbor not in visited:
                queue.append((neighbor, path + [neighbor]))

    return None  # Si aucun chemin n'est trouvé

# Algorithme DFS (Depth-First Search)
def dfs(start, goal, maze, directions):
    stack = [(start, [start])]  # Pile contenant la position actuelle et le chemin parcouru
    visited = set()  # Ensemble des positions déjà visitées

    while stack:
        current, path = stack.pop()
        if current == goal:
            return path  # Retourne le chemin si le but est atteint

        if current in visited:
            continue
        visited.add(current)

        # Explorer les voisins
        for neighbor in get_neighbors(current, maze, directions):
            if neighbor not in visited:
                stack.append((neighbor, path + [neighbor]))

    return None  # Si aucun chemin n'est trouvé

# Recherche du chemin avec BFS
print("\nRecherche de chemin avec BFS...")
bfs_path = bfs(start, goal, maze, directions)
if bfs_path:
    print("Chemin trouvé (BFS) :\n")
    afficher_labyrinthe(maze, taille_x, taille_y, bfs_path)
else:
    print("Aucun chemin trouvé avec BFS.")

# Recherche du chemin avec DFS
print("\nRecherche de chemin avec DFS...")
dfs_path = dfs(start, goal, maze, directions)
if dfs_path:
    print("Chemin trouvé (DFS) :\n")
    afficher_labyrinthe(maze, taille_x, taille_y, dfs_path)
else:
    print("Aucun chemin trouvé avec DFS.")
    
"""analyse et visualisation des algos"""
import time
import tracemalloc
import matplotlib.pyplot as plt

"""mesure de performances des deux algo"""
def measure_performance(algorithm, start, goal):
    start_time = time.time()
    tracemalloc.start()

    # Simuler un délai pour rendre le temps d'exécution visible
    time.sleep(0.001)

    path = algorithm(start, goal, maze, directions)

    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    elapsed_time = time.time() - start_time
    print(f"Algorithme: {algorithm.__name__}, Temps: {elapsed_time} s, Mémoire: {peak / 1024} KB")
    return path, elapsed_time, peak / 1024

"""Configuration des tests"""
algorithms = [
    (bfs, "BFS"),
    (dfs, "DFS"),
]

# Dictionnaire pour stocker les chemins trouvés
paths = {}

# Exécution des mesures
results = []
for algo, name in algorithms:
    path, time_taken, mem_used = measure_performance(algo, start, goal)
    paths[name] = path
    results.append((name, len(path) if path else 0, time_taken, mem_used))
    print(f"Résultats pour {name}: Path={path}, Time={time_taken}s, Memory={mem_used}KB")

# Affichage des résultats
fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(18, 5))

# Données pour les graphiques
names = [res[0] for res in results]
times = [res[2] * 1000 for res in results]  # en millisecondes
memory = [res[3] for res in results]
lengths = [res[1] for res in results]

# Graphique du temps d'exécution
ax1.bar(names, times, color='skyblue')
ax1.set_title("Temps d'exécution")
ax1.set_ylabel("Millisecondes")
ax1.grid(axis='y', linestyle='--')

# Graphique de la mémoire utilisée
ax2.bar(names, memory, color='lightgreen')
ax2.set_title("Mémoire utilisée")
ax2.set_ylabel("Kilobytes")
ax2.grid(axis='y', linestyle='--')

# Graphique de la longueur du chemin
ax3.bar(names, lengths, color='salmon')
ax3.set_title("Longueur du chemin")
ax3.set_ylabel("Nombre de nœuds")
ax3.grid(axis='y', linestyle='--')

plt.tight_layout()
plt.show()
