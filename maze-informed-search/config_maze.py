

def generate_maze(width, height, path, start, goal):#largeur #hauteur 
   
    maze = {} #le labyrinthe est stocker ici

    # Initialisation du labyrinthe avec des murs (1) 
    for y in range(height):
        for x in range(width):
            maze[(y, x)] = 1   #On remplit tout le labyrinthe avec des murs (1)

    # Assurer que le chemin prédéfini, le départ et l'arrivée sont libres (0)
    for coord in path:# On donne la valeur 0 aux coordonnées du chemin (path) 
        maze[coord] = 0 #passé par parametre

    maze[start] = 0
    maze[goal] = 0

    return maze
#Le code crée un chemin en forme de "L" étiré avec une queue
def initialize_path(path, width, height):
  
    i, j = 0, 0 # les coordonnées (x,y) position labyrinthe 
    for i in range(0, height // 2):
        path.append((i, j))

    for j in range(0, int(width / 2)):
        path.append((i, j))

    for i in range(0, height // 2):
        path.append((i, j))

    for j in range(width // 2, width - 1):
        path.append((0, j))

    for i in range(0, height):
        path.append((i, width - 1))  # Attention : width-1 pour éviter les dépassements

    return path

# Example maze configuration
path = []
width = 20
height = 20
path = initialize_path(path, width, height)
start = (0, 0)
goal = (height-1, width-1)
maze = generate_maze(width, height, path, start, goal)



