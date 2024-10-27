import random
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib import font_manager
from matplotlib.widgets import Button
from bull import moveBull
from robot import moveRobot
from grid_size import GRID_SIZE

plt.rcParams['font.family'] = 'Segoe UI Emoji'

MIN_WALL_LENGTH = 1
MAX_WALL_LENGTH = 4

def createEmptyGrid():
    return np.zeros((GRID_SIZE, GRID_SIZE))
#End createEmptyGrid

# Place target x in middle of grid
def placeTarget(grid):
    center = int(GRID_SIZE / 2)
    grid[center][center] = 3 # Value for target
    return center
# End placeTarget

def placeWallsAroundTarget(grid, targetRow, targetCol):
    """urround target with a wall and leave one random opening

    Args:
        grid (2d array): represents 2d array of possible locations for
        all possible world items
        targetRow (int): target row to place wall
        targetCol (int): target column to place wall
    """
    wallPositions = [
        (targetRow-1, targetCol-1), (targetRow-1, targetCol), (targetRow-1, targetCol+1),  # Top row
        (targetRow, targetCol-1),                         (targetRow, targetCol+1),  # Left and right
        (targetRow+1, targetCol-1), (targetRow+1, targetCol), (targetRow+1, targetCol+1)  # Bottom row
    ]
    
    # Choose random wall position to leave open
    corralWalls = set()
    corralPositions = {(targetRow, targetCol)}  # Track the two interior cells inside the corral

    # Set the walls around the target
    for i, (r, c) in enumerate(wallPositions):
        if (r == targetRow-1 and c == targetCol):  # This is the opening cell
            continue  # Leave this cell open (do not mark it as a wall)
        grid[r][c] = 1  # Wall value
        corralWalls.add((r, c))

    return corralWalls, corralPositions
# End placeWallsAroundTarget

def placeRandomWalls(grid):
    """ Places 3 to 7 random walls in the 13x13 grid

    Args:
        grid (2d array): represents 2d array of possible locations for
        all possible world items
    """
    numWalls = random.randint(3, 7)
    for _ in range(numWalls):
        # Choose random start position and direction (Make sure to add check for starting locations)
        startRow = random.randint(1, GRID_SIZE - 2)
        startCol = random.randint(1, GRID_SIZE - 2)
        wallLength = random.randint(MIN_WALL_LENGTH, MAX_WALL_LENGTH)
        direction = random.choice([(0, 1), (1, 0)]) # Horizontal or vertical
        
        # Place wall
        for i in range(wallLength):
            newRow = startRow + i * direction[0]
            newCol = startCol + i * direction[1]
            if 0 <= newRow < GRID_SIZE and 0 <= newCol < GRID_SIZE:
                if grid[newRow][newCol] == 0:
                    grid[newRow][newCol] = 1
# end placeRandom Walls

textAnnotations = []

# function to animate bull and robot movements
def animate(frame):
    # Clear previous bull and robot positions
    grid[bullPosition[0], bullPosition[1]] = 0
    grid[robotPosition[0], robotPosition[1]] = 0

    # Check if the bull reaches the target
    if bullPosition == [center, center]:
        print("The bull has reached the target!")
        text = plt.text(0.5, 0.5, "The bull has reached the target!", fontsize=18, ha='center', transform=plt.gcf().transFigure)
        plt.gca().figure.canvas.stop_event_loop()
        return [text]

    if robotPosition == bullPosition:
        print("The robot has died to the bull!")
        text = plt.text(0.5, 0.5, "The robot has died to the bull!", fontsize=18, ha='center', transform=plt.gcf().transFigure)
        plt.gca().figure.canvas.stop_event_loop()
        return [text]

    # Move robot and bull
    moveRobot(robotPosition, bullPosition, obstacles, corralWalls, corralPositions)
    moveBull(bullPosition, robotPosition, obstacles, corralPositions)

    # Update bull and robot positions on the grid
    grid[bullPosition[0], bullPosition[1]] = 2
    grid[robotPosition[0], robotPosition[1]] = 4
    
    mat.set_data(grid)
    
    while textAnnotations:
        annotation = textAnnotations.pop()
        annotation.remove()

    # Add emojis as text annotations on top of the grid
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            if grid[i][j] == 2:
                axis.text(j, i, "🐂", ha='center', va='center', fontsize=15)
            elif grid[i][j] == 4:
                axis.text(j, i, "🤖", ha='center', va='center', fontsize=15)
            elif grid[i][j] == 3:
                axis.text(j, i, "🏁", ha='center', va='center', fontsize=15)
    
    return [mat] + textAnnotations
# end animate

# Main function to create and animate grid with obstacles and walls
def createAndAnimateGrid():
    # Create grid and place target
    global grid, bullPosition, robotPosition, center, obstacles, mat, axis, corralPositions, corralWalls
    grid = createEmptyGrid()
    center = placeTarget(grid)
     
    corralWalls, corralPositions = placeWallsAroundTarget(grid, center, center)
    
    placeRandomWalls(grid)
    
    # Gather all positions that are walls
    obstacles = set((i, j) for i in range(GRID_SIZE) for j in range(GRID_SIZE) if grid[i, j] == 1)
    
    bullPosition = [0, 0]
    robotPosition = [GRID_SIZE - 1, GRID_SIZE - 1]
    
    grid[bullPosition[0], bullPosition[1]] = 2
    grid[robotPosition[0], robotPosition[1]] = 4
    
    # Create plot
    fig, axis = plt.subplots()
    mat = axis.matshow(grid, cmap='Set3')
    
    startButtonAx = plt.axes([0.8, 0.05, 0.15, 0.075])
    startButton = Button(startButtonAx, 'Start Rodeo')
    
    # Placeholder for animation object
    animation = None 
    
    def startAnimation(event):
        nonlocal animation
        if animation is None:
            animation = FuncAnimation(fig, animate, frames=1000, interval=500, blit=True)
            plt.draw()
    
    startButton.on_clicked(startAnimation)
    # Show plot
    plt.show()

if __name__ == "__main__":
    createAndAnimateGrid()