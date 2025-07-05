from time import sleep
import pygame
import random
import math
from collections import defaultdict

# Initialize Pygame
pygame.init()



# Screen dimensions
WIDTH, HEIGHT = 600, 400
TILE_SIZE = 40
ROWS, COLS = HEIGHT // TILE_SIZE, WIDTH // TILE_SIZE
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Rescue the Hostage - Local Search")

# Colors
WHITE = (240, 248, 255)
RED = (255, 69, 0)      # Hostage color
BLUE = (30, 144, 255)   # Player color
LIGHT_GREY = (211, 211, 211) # Background grid color
FLASH_COLOR = (50, 205, 50) # Victory flash color
BUTTON_COLOR = (50, 205, 50) # Button color
BUTTON_TEXT_COLOR = (255, 255, 255) # Button text color

# Load images for player, hostage, and walls
player_image = pygame.image.load("AI1.png")  
hostage_image = pygame.image.load("AI2.png")  
wall_images = [
    pygame.image.load("AI3.png"),
    pygame.image.load("AI4.png"),
    pygame.image.load("AI5.png")
]

# Resize images to fit the grid
wall_images = [pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE)) for img in wall_images]
player_image = pygame.transform.scale(player_image, (TILE_SIZE, TILE_SIZE))
hostage_image = pygame.transform.scale(hostage_image, (TILE_SIZE, TILE_SIZE))

# Constants for recent positions
MAX_RECENT_POSITIONS = 10
GENERATION_LIMIT = 50
MUTATION_RATE = 0.1

# Function to generate obstacles
def generate_obstacles(num_obstacles):
    obstacles = []
    while len(obstacles) < num_obstacles:
        new_obstacle = [random.randint(0, COLS-1), random.randint(0, ROWS-1)]
        if new_obstacle not in obstacles:  # Make sure obstacles are not overlapping
            obstacles.append(new_obstacle)
    print(obstacles)
    obstacle_images = [random.choice(wall_images) for _ in obstacles]
    return obstacles, obstacle_images

# Function to start a new game
def start_new_game():
    global player_pos, hostage_pos, recent_positions, obstacles, obstacle_images, temperature
    temperature = 100
    obstacles, obstacle_images = generate_obstacles(20)
    recent_positions = []

    # Generate player and hostage positions with a larger distance
    while True:
        player_pos = [random.randint(0, COLS-1), random.randint(0, ROWS-1)]
        hostage_pos = [random.randint(0, COLS-1), random.randint(0, ROWS-1)]
        distance = math.dist(player_pos, hostage_pos)
        if distance > 8 and player_pos not in obstacles and hostage_pos not in obstacles:
            break


def get_neighbors(player, obstacles):
    possible_moves = [[0, 1], [1, 0], [-1, 0], [0, -1]]
    neighbors = [[player[0] + move[0], player[1] + move[1]] for move in possible_moves
                  if [player[0] + move[0], player[1] + move[1]] not in obstacles
                    and player[0] + move[0] < COLS
                    and player[1] + move[1] < ROWS 
                    and player[0] + move[0] >= 0 and player[1] + move[1] >= 0]
    return neighbors
    

def calculate_dist(player, hostage):
    return abs(player[0] - hostage[0]) + abs(player[1] - hostage[1])

# Function to move the player closer to the hostage using Hill Climbing algorithm
def hill_climbing(player, hostage, obstacles):
    # current_dist = calculate_dist(player, hostage)
    # for i in neighbors:
    neighbors = get_neighbors(player, obstacles)
    best_neighbor = min(neighbors + [player], key=lambda x: calculate_dist(x, hostage))
    return best_neighbor

# Function for Simulated Annealing
def simulated_annealing(player, hostage, obstacles):
    global temperature
    cooling_rate = 0.96
    neighbors = get_neighbors(player, obstacles)
    selected_neighbor = random.choice(neighbors)
    selected_neighbor_cost = calculate_dist(selected_neighbor, hostage)
    player_cost = calculate_dist(player, hostage)
    probability = acceptance_probability(player_cost, selected_neighbor_cost, temperature)
    if random.random() < probability:
        if temperature > .1:
            temperature *= cooling_rate
        print(temperature)
        print()
        return selected_neighbor 
    else:
        return player

    # Acceptance probability function
def acceptance_probability(old_cost, new_cost, temp):
    delta = new_cost - old_cost
    prob = math.exp(-delta / temp) if delta > 0 else 1.0
    return prob
    #todo
    pass

class Graph:

    # Constructor
    def __init__(self):

        # Default dictionary to store graph
        self.graph = defaultdict(list)
        
    
    def addEdge(self, obstacles):
        for i in range(COLS):
            for j in range(ROWS):
                neighbors = get_neighbors([i, j], obstacles)
                for neighbor in neighbors:
                    self.graph[(i, j)].append(neighbor)
        # print(self.graph)
        
    def dfs_path(self, current, hostage_pos, visited, path):
        visited.add(tuple(current))
        path.append(tuple(current))
        if tuple(current) == hostage_pos:
            return path
        neighbors = self.graph[tuple(current)]
        shffled_neighbors = random.shuffle(neighbors)
        for neighbor in neighbors:
            if tuple(neighbor) not in visited:
                result = self.dfs_path(neighbor, hostage_pos, visited, path)
                if result:
                    return result
        
        path.pop()
        return None
    
    
    def DFS(self, player_pos, hostage_pos):
        visited = set()
        self.addEdge(obstacles)
        return self.dfs_path(player_pos, hostage_pos, visited, [])

    
# Function for Genetic Algorithm
def genetic_algorithm(player, hostage, obstacles):
    population_size = 20
    generations = 50

    # Fitness function
    def fitness(individual):
        dist = len(individual)
        # if dist == 0:
        #     print(individual)
        #     pass
        return pow(dist, -1)
    

    # Generate random population
    def generate_population(player, hostage):
        g = Graph()
        population = []
        for i in range(population_size):
            population.append(g.DFS(tuple(player), tuple(hostage)))
        return population
    
    def assign_weights(population):
        fitness_scores = [fitness(ind) for ind in population]
        total_fitness = sum(fitness_scores)
        weights = [score / total_fitness for score in fitness_scores]  # Normalize to probabilities
        return weights
    
    def select_parents(generation, weights):
        parents = random.choices(generation, weights=weights, k=population_size // 2)
        return parents
        
    
    # Crossover function
    def crossover(parent1, parent2):
        common_elements = [item for item in parent1 if item in parent2]
        # print(f"common_elements :{common_elements}")
        if not common_elements:
            return parent1, parent2
        
        common_coordinate = random.choice(common_elements)
        p1_common_idx = parent1.index(common_coordinate)
        p2_common_idx = parent2.index(common_coordinate)
        child1 = parent1[:p1_common_idx + 1] + parent2[p2_common_idx + 1:]
        child2 = parent2[:p2_common_idx + 1] + parent1[p1_common_idx + 1:]
        # print(f"common :{common_coordinate}")
        # print(f"p1 :{parent1}")
        # print(f"p2 :{parent2}")
        # print(f"c1 :{child1}")
        # print(f"c2 :{child2}")
        return child1, child2

    # Mutation function
    def mutate(individual):
        if random.random() < MUTATION_RATE:
            # Select a random index for mutation within the bounds of the individual
            mutation_idx = random.randint(0, len(individual) - 2)
            
            # Get the neighbors for the selected index
            neighbors = get_neighbors(individual[mutation_idx], obstacles)
            
            if neighbors:
                # Choose a random neighbor for the mutation point
                detour = random.choice(neighbors)
                
                # Ensure the detour does not repeat the immediate next position in the path
                if detour != individual[mutation_idx + 1]:
                    # Insert the detour in place of the next position
                    individual = individual[:mutation_idx + 1] + [detour] + individual[mutation_idx + 1:]

        # Return the mutated individual, ensuring path validity
        return individual[:ROWS * COLS]

    
    current_generation = generate_population(player, hostage)
    
    # best_parents = select_parents(current_generation, weights)
    
    for _ in range(generations):
        produced_genes = []
        weights = assign_weights(current_generation)
        # print(f"weights :{weights}")
        best_parents = select_parents(current_generation, weights)
        # print(f"best_parents :{best_parents}")
        
        for i in range(0, len(best_parents), 2) :
            if i+1 < len(best_parents) :
                child1, child2 = crossover(best_parents[i], best_parents[i+1])
                child1 = mutate(child1)
                child2 = mutate(child2)
                produced_genes.extend([child1, child2])
                # print(f"p :{produced_genes}")
        
        # produced_genes = [mutate(gene) for gene in produced_genes]
        # print(current_generation)
        # produced_genes = [mutate(gene) for gene in produced_genes]
        current_generation = produced_genes
    # print(f"p :{produced_genes}")
    # print(f"max is :{max(current_generation, key=fitness)}")
    return max(current_generation, key=fitness)
    

#Objective: Check if the player is stuck in a repeating loop.
def in_loop(recent_positions, player):
    if player in recent_positions[-10:]:
        return True
    return False
    #todo

#Objective: Make a random safe move to escape loops or being stuck.
def random_move(player, obstacles):
    
    neighbors = get_neighbors(player, obstacles)
    new_pos = random.choice(neighbors)
    return new_pos
    #todo
    pass

#Objective: Update the list of recent positions. 
def store_recent_position(recent_positions: list, new_player_pos, max_positions=MAX_RECENT_POSITIONS):
    recent_positions.append(new_player_pos)
    
    #todo
    # pass

# Function to show victory flash
def victory_flash():
    for _ in range(5):
        screen.fill(FLASH_COLOR)
        pygame.display.flip()
        pygame.time.delay(100)
        screen.fill(WHITE)
        pygame.display.flip()
        pygame.time.delay(100)

# Function to show a button and wait for player's input
def show_button_and_wait(message, button_rect):
    font = pygame.font.Font(None, 36)
    text = font.render(message, True, BUTTON_TEXT_COLOR)
    button_rect.width = text.get_width() + 20
    button_rect.height = text.get_height() + 10
    button_rect.center = (WIDTH // 2, HEIGHT // 2)
    pygame.draw.rect(screen, BUTTON_COLOR, button_rect)
    screen.blit(text, (button_rect.x + (button_rect.width - text.get_width()) // 2,
                       button_rect.y + (button_rect.height - text.get_height()) // 2))
    pygame.display.flip()
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if button_rect.collidepoint(event.pos):
                    waiting = False

# Function to get the algorithm choice from the player
def get_algorithm_choice():
    print("Choose an algorithm:")
    print("1: Hill Climbing")
    print("2: Simulated Annealing")
    print("3: Genetic Algorithm")
    while True:
        choice = input("Enter the number of the algorithm you want to use (1/2/3): ")
        if choice == "1":
            return hill_climbing
        elif choice == "2":
            return simulated_annealing
        elif choice == "3":
            return genetic_algorithm
        else:
            print("Invalid choice. Please choose 1, 2, or 3.")

# Main game loop
running = True
clock = pygame.time.Clock()
start_new_game()
button_rect = pygame.Rect(0, 0, 0, 0)
# genetic_algorithm(player_pos, hostage_pos, obstacles)
# sleep(5)
# Get the algorithm choice from the player
chosen_algorithm = get_algorithm_choice()
move_ctr = 0
while running:
    screen.fill(WHITE)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    if chosen_algorithm == genetic_algorithm:
        if move_ctr == 0 :
            genetic_path = genetic_algorithm(player_pos, hostage_pos, obstacles)
        new_player_pos = list(genetic_path[move_ctr])
        move_ctr += 1
    else:
        # Perform the chosen algorithm step
        new_player_pos = chosen_algorithm(player_pos, hostage_pos, obstacles)

        # Check for stuck situations
        if new_player_pos == player_pos or in_loop(recent_positions[-10:], new_player_pos):
            # Perform a random move when stuck
            new_player_pos = random_move(player_pos, obstacles)

    # Update recent positions
    store_recent_position(recent_positions, new_player_pos)
    # Update player's position
    player_pos = new_player_pos
    # Draw the grid background
    for row in range(ROWS):
        for col in range(COLS):
            rect = pygame.Rect(col * TILE_SIZE, row * TILE_SIZE, TILE_SIZE, TILE_SIZE)
            pygame.draw.rect(screen, LIGHT_GREY, rect, 1)

    # Draw obstacles
    for idx, obs in enumerate(obstacles):
        obs_rect = pygame.Rect(obs[0] * TILE_SIZE, obs[1] * TILE_SIZE, TILE_SIZE, TILE_SIZE)
        screen.blit(obstacle_images[idx], obs_rect)

    # Draw player
    player_rect = pygame.Rect(player_pos[0] * TILE_SIZE, player_pos[1] * TILE_SIZE, TILE_SIZE, TILE_SIZE)
    screen.blit(player_image, player_rect)

    # Draw hostage
    hostage_rect = pygame.Rect(hostage_pos[0] * TILE_SIZE, hostage_pos[1] * TILE_SIZE, TILE_SIZE, TILE_SIZE)
    screen.blit(hostage_image, hostage_rect)

    # Check if player reached the hostage
    if player_pos == hostage_pos:
        print("Hostage Rescued!")
        victory_flash()  # Show the victory flash
        show_button_and_wait("New Game", button_rect)
        move_ctr = 0
        start_new_game()

    # Update the display
    pygame.display.flip()
    clock.tick(10)  # Lower frame rate for smoother performance
    print(player_pos)
    # print(hostage_pos)
    # sleep(100)

pygame.quit()
