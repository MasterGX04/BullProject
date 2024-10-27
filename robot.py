import random
from grid_size import GRID_SIZE
ROBOT_MOVES = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (-1, -1), (1, -1), (-1, 1)]

def manhattanDistance(pos1, pos2):
    return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])

# Cache results for computed states to avoid redundant calculations
tStarCache = {}

# Recursive function to compute T* for given bull and robot position
def computeTStar(bullPosition, robotPosition, targetPosition, obstacles, corralPositions, maxDepth=50, depth=0):
    if depth > maxDepth:
        return float('inf')
    
    # Base case: If the robot reaches the target position, T* is zero
    if robotPosition == targetPosition:
        return 0

    # Checks if result is cached    
    state = (bullPosition[0], bullPosition[1], robotPosition[0], robotPosition[1])
    if state in tStarCache:
        return tStarCache[state]
    
    # Initialize the minimal T* value
    bestTStar = None

    # Explore all possible moves for the robot
    for move in ROBOT_MOVES:
        newRobotX = robotPosition[0] + move[0]
        newRobotY = robotPosition[1] + move[1]

        # Check if the move is within bounds and avoids obstacles and corral positions
        if (0 <= newRobotX < GRID_SIZE) and (0 <= newRobotY < GRID_SIZE) and \
           (newRobotX, newRobotY) not in obstacles and (newRobotX, newRobotY) not in corralPositions:
            
            # Next position for the robot after this move
            nextRobotPosition = [newRobotX, newRobotY]

            # Recursively calculate T* for the new position
            tStarValue = 1 + computeTStar(bullPosition, nextRobotPosition, targetPosition, obstacles, corralPositions, maxDepth, depth + 1)
            
            # Track the minimum T* value across possible moves
            if bestTStar is None or tStarValue < bestTStar:
                bestTStar = tStarValue
                
    bestTStar = bestTStar if bestTStar is not None else float('inf')
    return bestTStar

# Movement logic for robot
def moveRobot(robotPosition, bullPosition, targetPosition, obstacles, corralPositions):    
    global tStarCache
    tStarCache.clear()
    
    # Robot will move out of corral if it accidentally goes inside
    if tuple(robotPosition) in corralPositions:
        # Try to move out of the corral
        for move in ROBOT_MOVES:
            newRobotX = robotPosition[0] + move[0]
            newRobotY = robotPosition[1] + move[1]
            
            # Ensure new position is within bounds, not an obstacle, and outside the corral
            if (0 <= newRobotX < GRID_SIZE) and (0 <= newRobotY < GRID_SIZE) and \
               (newRobotX, newRobotY) not in obstacles and (newRobotX, newRobotY) not in corralPositions:
                robotPosition[0], robotPosition[1] = newRobotX, newRobotY
                print(f"Robot moved out of corral to position: {robotPosition}")
                return  # Exit immediately after moving out of corral
    
    # If robot is not within bull's 5x5 move towards bull
    if manhattanDistance(bullPosition, robotPosition) > 5:
        target = bullPosition
    else:
        target = targetPosition

    
    # Calculate robot's movement strategy by trying to move towards target
    bestMove = None
    bestTStar = float('inf')
    
    for move in ROBOT_MOVES:
        newRobotX = robotPosition[0] + move[0]
        newRobotY = robotPosition[1] + move[1]
        if (0 <= newRobotX < GRID_SIZE) and (0 <= newRobotY < GRID_SIZE) and \
           (newRobotX, newRobotY) not in obstacles and (newRobotX, newRobotY) not in corralPositions:
            
            # Compute T* for this potential move
            tStarValue = computeTStar(bullPosition, [newRobotX, newRobotY], target, obstacles, corralPositions)
            print(f"Tstar value: {tStarValue}")
            
            # Track the move that minimizes T*
            if tStarValue < bestTStar:
                bestMove = move
                bestTStar = tStarValue
                
        # Apply best move if iti exists
    if bestMove:
        robotPosition[0] += bestMove[0]
        robotPosition[1] += bestMove[1]
# end moveRobot                 