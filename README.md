# Local Search Hostage Rescue

## Overview
The **Hostage Rescue Game** is a 2D game developed using the **Pygame** library in Python. In this game, an agent navigates a grid-based environment to rescue a hostage while avoiding randomly placed obstacles. The game employs local search algorithms to guide the agent's movements toward the hostage, incorporating strategies to avoid obstacles and escape loops or dead-ends. The game features a graphical interface with visual representations of the agent, hostage, and obstacles, and includes victory animations and restart functionality.
![Screencast from 2025-07-05 18-08-58](https://github.com/user-attachments/assets/fe529240-46cc-44c8-9158-4b0e90fd4396)


## Features
1. **Game Initialization**:
   - The game window is created using Pygame with a defined grid size and cell dimensions.
   - Images for the agent, hostage, and obstacles are loaded and scaled to fit the grid cells.
   - The game window displays the title and initializes the environment.

2. **Obstacle Generation**:
   - Obstacles are randomly placed on the grid using the `generate_obstacles` function.
   - Obstacles are ensured not to overlap with each other or the agent/hostage positions.
   - Each obstacle is assigned a random image from a predefined set.

3. **New Game Setup**:
   - The `start_new_game` function initializes a new game by randomly placing the agent and hostage.
   - The distance between the agent and hostage is set to be at least 8 units to ensure a challenging yet solvable path (this value can be adjusted for testing).
   - Obstacles are regenerated for each new game.
   - The agent's recent positions are stored to detect and avoid loops.

4. **Victory and Restart**:
   - When the agent reaches the hostage, a victory message is displayed with a green flash effect for a few moments.
   - The game pauses, and a button allows the player to restart a new game.

5. **Main Game Loop**:
   - The game runs continuously until the window is closed.
   - In each frame:
     - The game board is redrawn.
     - The agent's new position is calculated based on the selected algorithm.
     - Victory or failure conditions are checked.
     - The frame rate is controlled using `clock.tick` (set to 5 FPS for smoother performance).

## Implemented Local Search Algorithms
The game implements three local search algorithms to navigate the agent toward the hostage, each with enhancements to handle dead-ends and avoid loops:

### 1. Hill Climbing
- **Basic Version**: The agent agent the neighboring cell that minimizes the distance to the hostage (greedy approach).
- **Dead-End Handling**: If the player reaches a dead-end (no valid move brings it closer to the hostage), a random valid move is chosen to escape the dead-end.
- **Loop Detection and Avoidance**: The player's recent positions are tracked. If the player repeats positions excessively (indicating a loop), a random valid move is made to break the cycle.

### 2. Simulated Annealing
- **Basic Version**: The agent can accept moves that increase the distance to the hostage with a probability based on a temperature parameter. The temperature decreases over time, making the algorithm increasingly greedy.
- **Dead-End Handling**: If no valid move brings the player closer to the hostage, a random valid move is chosen, though this is less frequent due to the algorithm's ability to naturally escape local minima through probabilistic moves.
- **Loop Detection and Avoidance**: Similar to Hill Climbing, repeated positions are detected, and a random valid move is applied to escape loops.

### 3. Genetic Algorithm
- **Basic Version**: A population of paths (sequences of moves) is generated. The best paths are selected, and crossover and mutation operations are applied to create new generations, converging toward an optimal path to the hostage.
- **Dead-End Handling**: If a path leads to a dead-end, increased mutation rates introduce random changes to explore alternative paths.
- **Loop Detection and Avoidance**: If the population converges to repeating paths (indicating a loop), random mutations are applied to diversify the paths and escape the loop.

## Installation
1. **Prerequisites**:
   - Python 3.x
   - Pygame library (`pip install pygame`)

2. **Setup**:
   - Clone or download the project repository.
   - Ensure the required image files for the player, hostage, and obstacles are in the project directory.
   - Install dependencies by running:
     ```bash
     pip install -r requirements.txt
     ```
     (Create a `requirements.txt` with `pygame` if not already present.)

3. **Running the Game**:
   - Navigate to the project directory.
   - Run the main game script:
     ```bash
     python main.py
     ```

## Usage
- Launch the game to start a new session.
- The player automatically moves toward the hostage using the selected local search algorithm.
- Avoid obstacles and watch for the victory animation when the hostage is reached.
- Click the restart button to begin a new game after a victory.
- Close the game window to exit.
