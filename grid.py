import random
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib import font_manager
from matplotlib.widgets import Button
from bull import moveBull
from robot import moveRobot
from global_functions import ROBOT_MOVES, GRID_SIZE, manhattanDistance

plt.rcParams['font.family'] = 'Segoe UI Emoji'

MIN_WALL_LENGTH = 1
MAX_WALL_LENGTH = 4

alpha = 0.1 # Learning rate
gamma = 0.9 # Discount factor
epsilon = 0.1 # Exploration rate
Q = {}

def getState(robotPosition, bullPosition):
    return (tuple(robotPosition), tuple(bullPosition))
# End getState

def updateQTable(state, action, reward, nextState):
    # initialize Q-values if state and action pair not inQ
    if (state, action) not in Q:
        Q[(state, action)] = 0
    
    maxQNext = max(Q.get((nextState, a), 0) for a in ROBOT_MOVES)
    
    # Use Q-learning rule to update Q-Value
    Q[(state, action)] += alpha * (reward + gamma * maxQNext - Q[(state, action)])

def chooseAction(state):
    # Epislon choice
    if random.uniform(0, 1) < epsilon:
        return random.choice(ROBOT_MOVES)
    else:
        qValues = [(Q.get((state, action), 0), action) for action in ROBOT_MOVES]
        maxQ, bestAction = max(qValues)
        return bestAction
# End chooseAction

def calculateReward(robotPosition, bullPosition, corralCenter, corralWalls):
    maxReward = 100
    collisionPenalty = -50
    stepPenalty = -1
    corralProximityReward = 10 # Reward multiplier for getting close to corral
    
    distanceToCorral = manhattanDistance(bullPosition, corralCenter)
    
    # Goal reward if bull is in corral
    if bullPosition == corralCenter:
        return maxReward
    
    if robotPosition == bullPosition:
        return collisionPenalty
    
    proximityReward = corralProximityReward / (distanceToCorral + 1)
    
    # Total reward from step penalty and proximity
    totalReward = proximityReward + stepPenalty
    return totalReward
# End calculateReward

def createEmptyGrid():
    return np.zeros((GRID_SIZE, GRID_SIZE))
#End createEmptyGrid

# Place target x in middle of grid
def placeTarget(grid):
    center = int(GRID_SIZE / 2)
    grid[center][center] = 3 # Value for target
    return center
# End placeTarget

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

iterationCount = 0
successfulAttempts = 0
textAnnotations = []
chargingDirection = None
# function to animate bull and robot movements
def animate(frame):
    global chargingDirection, iterationCount, successfulAttempts
    # Clear previous bull and robot positions
    grid[bullPosition[0], bullPosition[1]] = 0
    grid[robotPosition[0], robotPosition[1]] = 0
    iterationCount += 1

    # Check if the bull reaches the target
    if bullPosition == [center, center]:
        print("The bull has reached the target!")
        successfulAttempts += 1
        print(f'Number of steps it took: {iterationCount}\nSuccessful Attempts: {successfulAttempts}')
        iterationCount = 0
        
        bullPosition[:] = [0, 0] # Reset bull position
        robotPosition[:] = [GRID_SIZE - 1, GRID_SIZE - 1]
        grid[bullPosition[0], bullPosition[1]] = 2
        grid[bullPosition[0], bullPosition[1]] = 4
        grid[center, center] = 3
        return [mat]

    if robotPosition == bullPosition:
        print("The robot has died to the bull!")
        iterationCount = 0
        
        bullPosition[:] = [0, 0] # Reset bull position
        robotPosition[:] = [GRID_SIZE - 1, GRID_SIZE - 1]
        grid[bullPosition[0], bullPosition[1]] = 2
        grid[robotPosition[0], robotPosition[1]] = 4
        return [mat]

    # Choose an action and move robot
    currentState = getState(robotPosition, bullPosition)
    action = chooseAction(currentState)
    # Step 1: Move the robot first
    moveRobot(robotPosition, bullPosition, obstacles, corralWalls, corralPositions)
    
    # Update the grid with the robot's new position before moving the bull
    grid[robotPosition[0], robotPosition[1]] = 4
    
    # Step 2: Move the bull after the robot has moved
    chargingDirection = moveBull(bullPosition, robotPosition, obstacles, chargingDirection)
    
    # Next state and reward
    nextState = getState(robotPosition, bullPosition)
    reward = calculateReward(robotPosition, bullPosition, [center, center], corralWalls) # Update
    
    updateQTable(currentState, action, reward, nextState)
    
    # Update bull's position on the grid
    grid[bullPosition[0], bullPosition[1]] = 2
    
    # Update the grid display
    mat.set_data(grid)

    return [mat]
# end animate

# Main function to create and animate grid with obstacles and walls
def createAndAnimateGrid():
    # Create grid and place target
    global grid, bullPosition, robotPosition, center, obstacles, mat, axis, corralPositions, corralWalls
    grid = createEmptyGrid()
    center = placeTarget(grid)
     
    corralWalls, corralPositions = placeWallsAroundTarget(grid, center, center)
    
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