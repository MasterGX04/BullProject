import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.widgets import Button
from grid_size import GRID_SIZE
from MDProbot import MDPGrid
from bull import moveBull

plt.rcParams['font.family'] = 'Segoe UI Emoji'

def createEmptyGrid():
    return np.zeros((GRID_SIZE, GRID_SIZE))

def placeTarget(grid):
    center = int(GRID_SIZE / 2)
    grid[center][center] = 3  # Value for target
    return center

def placeWallsAroundTarget(grid, targetRow, targetCol):
    wallPositions = [
        (targetRow-1, targetCol-1), (targetRow-1, targetCol), (targetRow-1, targetCol+1),
        (targetRow, targetCol-1),                         (targetRow, targetCol+1),
        (targetRow+1, targetCol-1), (targetRow+1, targetCol), (targetRow+1, targetCol+1)
    ]
    
    corralWalls = set()
    corralPositions = {(targetRow, targetCol)}  # Track interior cells

    for i, (r, c) in enumerate(wallPositions):
        if (r == targetRow-1 and c == targetCol):
            continue  # Leave this cell open
        grid[r][c] = 1  # Wall value
        corralWalls.add((r, c))

    return corralWalls, corralPositions

def animate(frame):
    global robotPosition, bullPosition, mdp, grid, obstacles
    grid[bullPosition[0], bullPosition[1]] = 0
    grid[robotPosition[0], robotPosition[1]] = 0

    # Transition robot and bull positions
    robotPosition, bullPosition = mdp.transition(tuple(robotPosition), tuple(bullPosition))

    # Move the bull according to its logic
    bullPosition = moveBull(bullPosition, robotPosition, obstacles, mdp.corral)

    # Update the grid with the new positions
    grid[robotPosition[0], robotPosition[1]] = 4  # Robot value
    grid[bullPosition[0], bullPosition[1]] = 2    # Bull value

    # Debugging print
    print(f"Robot Position: {robotPosition}, Bull Position: {bullPosition}")

    # Update the display
    mat.set_data(grid)

    # Check for end conditions
    if bullPosition in mdp.corral:
        plt.text(0.5, 0.5, "The bull has reached the target!", fontsize=18, ha='center', transform=plt.gcf().transFigure)
        plt.gca().figure.canvas.stop_event_loop()

    if robotPosition == bullPosition:
        plt.text(0.5, 0.5, "The robot has died to the bull!", fontsize=18, ha='center', transform=plt.gcf().transFigure)
        plt.gca().figure.canvas.stop_event_loop()

    return [mat]

def createAndAnimateGrid():
    global grid, bullPosition, robotPosition, center, mat, mdp, obstacles
    grid = createEmptyGrid()
    center = placeTarget(grid)
    
    corralWalls, corralPositions = placeWallsAroundTarget(grid, center, center)
    
    # Initialize MDPGrid
    mdp = MDPGrid(GRID_SIZE, center, center)
    obstacles = corralWalls  # Define obstacles as walls

    # Define starting positions
    bullPosition = [0, 0]
    robotPosition = [GRID_SIZE - 1, GRID_SIZE - 1]
    
    grid[bullPosition[0], bullPosition[1]] = 2
    grid[robotPosition[0], robotPosition[1]] = 4
    
    fig, axis = plt.subplots()
    mat = axis.matshow(grid, cmap='Set3')
    
    startButtonAx = plt.axes([0.8, 0.05, 0.15, 0.075])
    startButton = Button(startButtonAx, 'Start Rodeo')

    animation = None 
    
    def startAnimation(event):
        nonlocal animation
        if animation is None:
            animation = FuncAnimation(fig, animate, frames=1000, interval=500, blit=True)
            plt.draw()
    
    startButton.on_clicked(startAnimation)
    plt.show()

if __name__ == "__main__":
    createAndAnimateGrid()
