import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.widgets import Button
from global_functions import GRID_SIZE
from MDProbot import MDPGrid
from bull import moveBull
from utils import placeTarget, calculateReward
from collections import defaultdict

plt.rcParams['font.family'] = 'Segoe UI Emoji'

def createEmptyGrid():
    return np.zeros((GRID_SIZE, GRID_SIZE))

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

def getActionFromPolicy(policy, robotPosition, bullPosition):
    """
    Fetch the action from the policy for the given robot and bull positions.

    Parameters:
        policy (dict): The policy dict from value iteration.
        robot_position (tuple): The current robot position (row, col).
        bull_position (tuple): The current bull position (row, col).

    Returns:
        tuple: The action to take as (delta_row, delta_col).
    """
    state = (robotPosition, bullPosition)
    return policy.get(state, (0, 0))

def calculateGridRewards(targetPosition):
    allRewards = defaultdict(int)
    
    for robotRow in range(GRID_SIZE):
        for robotCol in range(GRID_SIZE):
            robotPosition = (robotRow, robotCol)
            
            if robotPosition == targetPosition:
                continue
            
            for bullRow in range(GRID_SIZE):
                for bullCol in range(GRID_SIZE):
                    bullPosition = (bullRow, bullCol)
                    
                    if bullPosition == robotPosition:
                        continue
                    
                    allRewards[(robotPosition, bullPosition)] = calculateReward(robotPosition, bullPosition, targetPosition)

    return allRewards
# End calculateGridRewards

def animate(frame):
    global robotPosition, bullPosition, mdp, grid, obstacles
    grid[bullPosition[0], bullPosition[1]] = 0
    grid[robotPosition[0], robotPosition[1]] = 0

    # Transition robot and bull positions
    optimalAction = mdp.policy.get((tuple(robotPosition), tuple(bullPosition)), (0, 0))  # Default to no movement if state not found

    # Update the robot position using the optimal action
    robotPosition = (robotPosition[0] + optimalAction[0], robotPosition[1] + optimalAction[1])
    
    # Move the bull according to its logic
    bullPosition = moveBull(bullPosition, robotPosition, obstacles, (GRID_SIZE // 2 - 2, GRID_SIZE // 2))

    # Update the grid with the new positions
    grid[robotPosition[0], robotPosition[1]] = 4  # Robot value
    grid[bullPosition[0], bullPosition[1]] = 2    # Bull value

    # Debugging print
    # print(f"Robot Position: {robotPosition}, Bull Position: {bullPosition}")

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
    
    # Unpack center tuple into row and column
    center_row, center_col = center
    corralWalls, corralPositions = placeWallsAroundTarget(grid, center_row, center_col)
    
    # Calculates all possible rewards based on bull and robot positions
    allRewards = calculateGridRewards(center)
    
    # Initialize MDPGrid
    mdp = MDPGrid(GRID_SIZE, center_row, center_col, allRewards)
    mdp.policy, _ = mdp.value_iteration()
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
