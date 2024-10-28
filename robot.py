from grid_size import GRID_SIZE
from collections import deque
from bull import isWithin5x5Square
ROBOT_MOVES = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (-1, -1), (1, -1), (-1, 1)]
DIAGONAL_MOVES = [(-1, -1), (-1, 1), (1, -1), (1, 1)]

def manhattanDistance(pos1, pos2):
    return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])

# Cache results for computed states to avoid redundant calculations
tStarCache = {}

# Recursive function to compute T* for given bull and robot position
def moveToTarget(robotPosition, targetPosition, obstacles, corralPositions):
    if robotPosition == targetPosition:
        return 0

    queue = deque([(robotPosition, 0)])  # Queue holds (position, distance) tuples
    visited = set([tuple(robotPosition)])  # Track visited positions to avoid cycles

    state = (tuple(robotPosition), tuple(targetPosition))
    if state in tStarCache:
        return tStarCache[state]
    
    adjacentToTarget = {
        (targetPosition[0] - 1, targetPosition[1]),  # Up
        (targetPosition[0] + 1, targetPosition[1]),  # Down
        (targetPosition[0], targetPosition[1] - 1),  # Left
        (targetPosition[0], targetPosition[1] + 1),  # Right
    }
    
    while queue:
        currentPosition, distance = queue.popleft()
        
        for move in ROBOT_MOVES:
            newRobotX = currentPosition[0] + move[0]
            newRobotY = currentPosition[1] + move[1]
            nextPosition = (newRobotX, newRobotY)

            if nextPosition == tuple(targetPosition):
                tStarCache[state] = distance + 1
                return distance + 1  # Reached the target
            
            if (0 <= newRobotX < GRID_SIZE) and (0 <= newRobotY < GRID_SIZE) and \
               nextPosition not in obstacles and nextPosition not in corralPositions and \
               nextPosition not in adjacentToTarget and nextPosition not in visited:
                
                visited.add(nextPosition)
                queue.append((nextPosition, distance + 1))
    
    tStarCache[state] = 10000
    return 10000  # If target is unreachable, return high value

# Movement logic for robot
def moveRobot(robotPosition, bullPosition, obstacles, corralWalls, corralPositions):    
    # Check if the bull is directly adjacent to the robot (danger zone)
    bullAdjacent = bullAdjacent = (abs(bullPosition[0] - robotPosition[0]) <= 1) and (abs(bullPosition[1] - robotPosition[1]) <= 1)
    
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
                   
    if bullAdjacent:
        for move in DIAGONAL_MOVES:
            newRobotX = robotPosition[0] + move[0]
            newRobotY = robotPosition[1] + move[1]
            
            # Calculate the new position
            newPosition = (newRobotX, newRobotY)

            # Ensure the move is within bounds, avoids obstacles, corral, and bull’s position
            if (0 <= newRobotX < GRID_SIZE) and (0 <= newRobotY < GRID_SIZE) and \
               newPosition not in obstacles and newPosition not in corralWalls and \
               newPosition not in corralPositions and newPosition != tuple(bullPosition):
                
                if abs(newRobotX - bullPosition[0]) > 1 or abs(newRobotY - bullPosition[1]) > 1:
                    robotPosition[0], robotPosition[1] = newRobotX, newRobotY
                    return
            
    # If robot is not within bull's 5x5 move towards bull
    if not isWithin5x5Square(bullPosition, robotPosition):
        target = bullPosition
    else:
        target = nearestCorralWall(robotPosition, corralWalls)
    
    # Calculate robot's movement strategy by trying to move towards target
    bestMove = None
    safeMoves = []
    minTStar = float('inf')
    
    for move in ROBOT_MOVES:
        newRobotX = robotPosition[0] + move[0]
        newRobotY = robotPosition[1] + move[1]
        if (0 <= newRobotX < GRID_SIZE) and (0 <= newRobotY < GRID_SIZE) and \
           (newRobotX, newRobotY) not in obstacles and (newRobotX, newRobotY) not in corralPositions and (newRobotX, newRobotY) != bullPosition:
            
            if abs(newRobotX - bullPosition[0]) > 1 or abs(newRobotY - bullPosition[1]) > 1:
                # Compute T* for this potential move
                tStarValue = moveToTarget([newRobotX, newRobotY], target, obstacles, corralPositions)
                safeMoves.append((move, tStarValue))
            else:
                tStarValue = moveToTarget([newRobotX, newRobotY], target, obstacles, corralPositions)
                if tStarValue < minTStar:
                    minTStar = tStarValue
                    bestMove = move
                
    # Apply best move if iti exists
    if safeMoves:
        bestSafeMove = min(safeMoves, key=lambda m: m[1])[0]
        robotPosition[0] += bestSafeMove[0]
        robotPosition[1] += bestSafeMove[1]
    elif bestMove:
        # If no safe moves exist, use the best available move to minimize T*
        robotPosition[0] += bestMove[0]
        robotPosition[1] += bestMove[1]
# end moveRobot               

# Helper function to find the nearest corral wall cell as the robot's target
def nearestCorralWall(robotPosition, corralWalls):
    nearestWall = min(corralWalls, key=lambda pos: manhattanDistance(robotPosition, pos))
    return nearestWall  