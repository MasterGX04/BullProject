import random
import numpy as np
import robot
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.widgets import Button
from bull import moveBull
from robot import moveRobot
from global_functions import ROBOT_MOVES, GRID_SIZE, manhattanDistance

plt.rcParams['font.family'] = 'Segoe UI Emoji'

alpha = 0.1  # Learning rate
gamma = 0.9  # Discount factor
epsilon = 0.1  # Exploration rate
Q = {}

def getState(robotPosition, bullPosition):
    return (tuple(robotPosition), tuple(bullPosition))

def updateQTable(state, action, reward, nextState):
    if (state, action) not in Q:
        Q[(state, action)] = 0
    maxQNext = max(Q.get((nextState, a), 0) for a in ROBOT_MOVES)
    Q[(state, action)] += alpha * (reward + gamma * maxQNext - Q[(state, action)])

def chooseAction(state):
    if random.uniform(0, 1) < epsilon:
        return random.choice(ROBOT_MOVES)
    else:
        qValues = [(Q.get((state, action), 0), action) for action in ROBOT_MOVES]
        maxQ, bestAction = max(qValues)
        return bestAction

def calculateReward(robotPosition, bullPosition, corralCenter, corralWalls):
    maxReward = 100
    collisionPenalty = -50
    stepPenalty = -1
    corralProximityReward = 10

    distanceToCorral = manhattanDistance(bullPosition, corralCenter)
    if bullPosition == corralCenter:
        return maxReward
    if robotPosition == bullPosition:
        return collisionPenalty
    proximityReward = corralProximityReward / (distanceToCorral + 1)
    totalReward = proximityReward + stepPenalty
    return totalReward

def createEmptyGrid():
    return np.zeros((GRID_SIZE, GRID_SIZE))

def placeTarget(grid):
    center = int(GRID_SIZE / 2)
    grid[center][center] = 3
    return center

def placeWallsAroundTarget(grid, targetRow, targetCol):
    wallPositions = [
        (targetRow - 1, targetCol - 1), (targetRow - 1, targetCol), (targetRow - 1, targetCol + 1),
        (targetRow, targetCol - 1), (targetRow, targetCol + 1),
        (targetRow + 1, targetCol - 1), (targetRow + 1, targetCol), (targetRow + 1, targetCol + 1)
    ]
    corralWalls = set()
    for i, (r, c) in enumerate(wallPositions):
        if (r == targetRow - 1 and c == targetCol):
            continue
        grid[r][c] = 1
        corralWalls.add((r, c))
    return corralWalls, (targetRow, targetCol)

successfulAttempts = 0
chargingDirection = None
iterationCount = 0
animation = None  # Placeholder for the animation instance

def animate(frame):
    global chargingDirection, iterationCount, successfulAttempts, animation
    iterationCount += 1
    grid[bullPosition[0], bullPosition[1]] = 0
    grid[robotPosition[0], robotPosition[1]] = 0

    if bullPosition == [center, center]:
        print("The bull has reached the target!")
        print("The T_star value at the start position/expected time where the Bull is at (0,0) and Robot is at (12,12):")
        print(T_star[((0,0),(12, 12))])
        successfulAttempts += 1
        print(f'Number of steps it took: {iterationCount}')
        if animation is not None:
            animation.event_source.stop()
        return [mat]

    moveRobot(robotPosition, bullPosition, policy)
    grid[robotPosition[0], robotPosition[1]] = 4
    chargingDirection = moveBull(bullPosition, robotPosition, obstacles, chargingDirection)
    grid[bullPosition[0], bullPosition[1]] = 2
    mat.set_data(grid)
    return [mat]

def createAndAnimateGrid():
    global grid, bullPosition, robotPosition, center, obstacles, mat, axis, corralWalls, policy, T_star, animation
    grid = createEmptyGrid()
    center = placeTarget(grid)
    corralWalls, corralPositions = placeWallsAroundTarget(grid, center, center)
    T_star, policy = robot.value_iteration(GRID_SIZE, 50, 0.0001, corralPositions, corralWalls)
    obstacles = set((i, j) for i in range(GRID_SIZE) for j in range(GRID_SIZE) if grid[i, j] == 1)
    bullPosition = [0, 0]
    robotPosition = [GRID_SIZE - 1, GRID_SIZE - 1]
    grid[bullPosition[0], bullPosition[1]] = 2
    grid[robotPosition[0], robotPosition[1]] = 4
    fig, axis = plt.subplots()
    mat = axis.matshow(grid, cmap='Set3')
    startButtonAx = plt.axes([0.8, 0.05, 0.15, 0.075])
    startButton = Button(startButtonAx, 'Start Rodeo')

    def startAnimation(event):
        global animation
        if animation is None:
            animation = FuncAnimation(fig, animate, frames=1, interval=500, blit=True)
            plt.draw()

    startButton.on_clicked(startAnimation)
    plt.show()

if __name__ == "__main__":
    createAndAnimateGrid()