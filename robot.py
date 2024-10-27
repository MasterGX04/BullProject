from grid_size import GRID_SIZE
from collections import deque
from bull import isWithin5x5Square
ROBOT_MOVES = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (-1, -1), (1, -1), (-1, 1)]

def manhattanDistance(pos1, pos2):
    return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])

# Cache results for computed states to avoid redundant calculations
tStarCache = {}

# Recursive function to compute T* for given bull and robot position
def computeTStar(robotPosition, targetPosition, obstacles, corralPositions):
    if robotPosition == targetPosition:
        return 0

    queue = deque([(robotPosition, 0)])  # Queue holds (position, distance) tuples
    visited = set([tuple(robotPosition)])  # Track visited positions to avoid cycles

    while queue:
        currentPosition, distance = queue.popleft()
        
        for move in ROBOT_MOVES:
            newRobotX = currentPosition[0] + move[0]
            newRobotY = currentPosition[1] + move[1]
            nextPosition = (newRobotX, newRobotY)

            if nextPosition == tuple(targetPosition):
                return distance + 1  # Reached the target
            
            if (0 <= newRobotX < GRID_SIZE) and (0 <= newRobotY < GRID_SIZE) and \
               nextPosition not in obstacles and nextPosition not in corralPositions and \
               nextPosition not in visited:
                
                visited.add(nextPosition)
                queue.append((nextPosition, distance + 1))
    
    return 10000  # If target is unreachable, return high value

# Movement logic for robot
def moveRobot(robotPosition, bullPosition, obstacles, corralWalls, corralPositions):    
    
    # Robot will move out of corral if it accidentally goes inside
    if tuple(robotPosition) in corralPositions:
        # Try to move out of the corral
        for move in ROBOT_MOVES:
            newRobotX = robotPosition[0] + move[0]
            newRobotY = robotPosition[1] + move[1]
            
            # Ensure new position is within bounds, not an obstacle, and outside the corral
            if (0 <= newRobotX < GRID_SIZE) and (0 <= newRobotY < GRID_SIZE) and \
               (newRobotX, newRobotY) not in obstacles and (newRobotX, newRobotY) not in corralPositions \
                (newRobotX, newRobotY) not in corralWalls:
                robotPosition[0], robotPosition[1] = newRobotX, newRobotY
                return  # Exit immediately after moving out of corral
    
    # If robot is not within bull's 5x5 move towards bull
    if not isWithin5x5Square(bullPosition, robotPosition):
        target = bullPosition
    else:
        target = nearestCorralWall(robotPosition, corralWalls)
    
    # Calculate robot's movement strategy by trying to move towards target
    bestMove = None
    bestTStar = float('inf')
    safeMoves = []
    
    for move in ROBOT_MOVES:
        newRobotX = robotPosition[0] + move[0]
        newRobotY = robotPosition[1] + move[1]
        if (0 <= newRobotX < GRID_SIZE) and (0 <= newRobotY < GRID_SIZE) and \
           (newRobotX, newRobotY) not in obstacles and (newRobotX, newRobotY) not in corralPositions:
            
            if (newRobotX, newRobotY) != tuple(bullPosition):
                safeMoves.append((move, newRobotX, newRobotY))
                
            # Compute T* for this potential move
            tStarValue = computeTStar([newRobotX, newRobotY], target, obstacles, corralPositions)
            #print(f'tStar Value for {move}: {tStarValue}')
            # Track the move that minimizes T*
            if tStarValue < bestTStar:
                bestMove = move
                bestTStar = tStarValue
                
    # Apply best move if iti exists
    if safeMoves:
        bestSafeMove = min(safeMoves, key=lambda m: computeTStar([m[1], m[2]], target, obstacles, corralPositions))
        robotPosition[0] += bestSafeMove[0][0]
        robotPosition[1] += bestSafeMove[0][1]
    elif bestMove:
        # If no safe moves exist, use the best available move to minimize T*
        robotPosition[0] += bestMove[0]
        robotPosition[1] += bestMove[1]
# end moveRobot               

# Helper function to find the nearest corral wall cell as the robot's target
def nearestCorralWall(robotPosition, corralWalls):
    nearestWall = min(corralWalls, key=lambda pos: manhattanDistance(robotPosition, pos))
    return nearestWall  