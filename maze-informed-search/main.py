#dans le fichier alog.py
import time
import tracemalloc
from collections import deque 
import heapq
#dans le fichier visualisation.py
import matplotlib.pyplot as plt
from math import pi

"""importer les fonctions des modules pour les utilisers"""
from algorithms import a_star, glouton, bfs, dfs, heuristic
from config_maze import maze, start, goal
from visualisation import plot_maze, plot_metrics


def main():
    # Afficher le labyrinthe initial
    print("Affichage du labyrinthe initial...")
    plot_maze(maze, title="Labyrinthe initial")
    
    # Exécuter tous les algorithmes
    algorithms = [
        ("A*", a_star),
        ("Glouton", glouton),
        ("BFS", bfs),
        ("DFS", dfs)
    ]
    
    results = []
    
    for name, algorithm in algorithms:
        print(f"\nExécution de l'algorithme {name}...")
        if name in ["A*", "Glouton"]:
            path, metrics = algorithm(start, goal, maze, heuristic)
        else:
            path, metrics = algorithm(start, goal, maze)
        
        results.append((name, path, metrics))
        
        # Afficher le labyrinthe avec le chemin trouvé
        plot_maze(maze, path, title=f"Labyrinthe - Algorithme {name}")
        
        # Afficher les métriques
        plot_metrics(metrics, name)
    
    # Comparaison des temps d'exécution finaux
    final_times = [metrics['time'][-1] for (_, _, metrics) in results]
    algorithm_names = [name for (name, _, _) in results]
    
    plt.figure(figsize=(10, 5))
    plt.bar(algorithm_names, final_times, color=['blue', 'green', 'red', 'purple'])
    plt.title("Comparaison des temps d'exécution finaux")
    plt.ylabel("Temps (secondes)")
    plt.show()
    
    # Comparaison de la mémoire utilisée maximale
    max_memory = [max(metrics['memory']) for (_, _, metrics) in results]
    
    plt.figure(figsize=(10, 5))
    plt.bar(algorithm_names, max_memory, color=['blue', 'green', 'red', 'purple'])
    plt.title("Comparaison de l'utilisation mémoire maximale")
    plt.ylabel("Mémoire (KB)")
    plt.show()
    
    # Afficher les résultats textuels
    print("\nRésumé des performances:")
    for name, path, metrics in results:
        print(f"\n{name}:")
        print(f"- Longueur du chemin: {len(path)} cases")
        print(f"- Temps total: {metrics['time'][-1]:.4f} secondes")
        print(f"- Mémoire maximale utilisée: {max(metrics['memory']):.2f} KB")

if __name__ == "__main__":
    main()