import matplotlib.pyplot as plt
from math import pi

def plot_maze(maze, path=None, title="Maze"):
    """Plot the maze with optional path."""
    if not maze:
        return
    
    # Extract coordinates and values
    rows = [coord[0] for coord in maze.keys()]
    cols = [coord[1] for coord in maze.keys()]
    values = [maze[coord] for coord in maze.keys()]
    
    # Determine maze dimensions
    height = max(rows) + 1
    width = max(cols) + 1
    
    # Create a grid representation
    grid = [[1 for _ in range(width)] for _ in range(height)]
    for (y, x), val in maze.items():
        grid[y][x] = val
    
    # Plot the maze
    plt.figure(figsize=(10, 10))
    plt.imshow(grid, cmap='binary', interpolation='nearest')
    
    # Mark start (green) and goal (red)
    start = next(coord for coord, val in maze.items() if val == 0 and coord == (0, 0))  # Adjust if start is different
    goal = next(coord for coord, val in maze.items() if val == 0 and coord == (height-1, width-1))  # Adjust if goal is different
    
    plt.plot(start[1], start[0], 'go', markersize=10)  # Start = green circle
    plt.plot(goal[1], goal[0], 'ro', markersize=10)    # Goal = red circle
    
    # Draw the path if provided
    if path:
        path_y, path_x = zip(*path)
        plt.plot(path_x, path_y, 'b-', linewidth=2)  # Path = blue line
    
    plt.title(title)
    plt.xticks(range(width))
    plt.yticks(range(height))
    plt.grid(which='both', color='gray', linestyle='-', linewidth=0.5)
    plt.show()

def plot_metrics(metrics, algorithm_name):
    """Plot time and memory usage metrics for an algorithm."""
    plt.figure(figsize=(12, 5))
    
    # Time plot
    plt.subplot(1, 2, 1)
    plt.plot(metrics['time'], 'b-', label='Time per step')
    plt.xlabel('Step')
    plt.ylabel('Time (seconds)')
    plt.title(f'{algorithm_name} - Time Evolution')
    plt.legend()
    
    # Memory plot
    plt.subplot(1, 2, 2)
    plt.plot(metrics['memory'], 'r-', label='Memory per step')
    plt.xlabel('Step')
    plt.ylabel('Memory (KB)')
    plt.title(f'{algorithm_name} - Memory Usage')
    plt.legend()
    
    plt.tight_layout()
    plt.show()

def plot_radar_chart(df):
    """Graphique radar comparant les performances normalisées"""
    # Normalisation des données
    metrics = ['time', 'memory', 'path_length']
    stats = df.groupby('algorithm')[metrics].mean()
    stats_norm = (stats - stats.min()) / (stats.max() - stats.min())
    
    # Configuration
    categories = list(stats_norm.columns)
    N = len(categories)
    angles = [n / N * 2 * pi for n in range(N)]
    angles += angles[:1]
    
    # Dessin
    plt.figure(figsize=(6, 6))
    ax = plt.subplot(111, polar=True)
    
    for algo in stats_norm.index:
        values = stats_norm.loc[algo].values.flatten().tolist()
        values += values[:1]
        ax.plot(angles, values, label=algo)
        ax.fill(angles, values, alpha=0.1)
    
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(categories)
    plt.title('Comparaison des algorithmes (0=meilleur, 1=pire)')
    plt.legend()
    plt.show()

def plot_bar_comparison(df):
    """Diagrammes à barres avec moyennes et écarts-types"""
    metrics = ['time', 'memory', 'path_length']
    titles = ['Temps (s)', 'Mémoire (KB)', 'Longueur chemin']
    
    plt.figure(figsize=(12, 4))
    
    for i, metric in enumerate(metrics):
        plt.subplot(1, 3, i+1)
        means = df.groupby('algorithm')[metric].mean()
        stds = df.groupby('algorithm')[metric].std()
        
        plt.bar(means.index, means, yerr=stds, capsize=5, alpha=0.7)
        plt.title(titles[i])
        plt.ylabel(metric)
    
    plt.tight_layout()
    plt.show()

def plot_boxplots(df):
    """Boîtes à moustaches pour chaque métrique"""
    metrics = ['time', 'memory', 'path_length']
    
    plt.figure(figsize=(12, 5))
    for i, metric in enumerate(metrics):
        plt.subplot(1, 3, i+1)
        df.boxplot(column=metric, by='algorithm', vert=False)
        plt.title(metric)
        plt.suptitle('')
    
    plt.tight_layout()
    plt.show()

def plot_pie_charts(df):
    """Diagrammes circulaires par algorithme"""
    algorithms = df['algorithm'].unique()
    metrics = ['time', 'memory', 'path_length']
    
    plt.figure(figsize=(15, 4))
    
    for i, algo in enumerate(algorithms):
        data = df[df['algorithm'] == algo][metrics].mean()
        plt.subplot(1, len(algorithms), i+1)
        plt.pie(data, labels=metrics, autopct='%1.1f%%')
        plt.title(algo)
    
    plt.tight_layout()
    plt.show()

