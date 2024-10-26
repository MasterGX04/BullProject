import random
from grid_size import GRID_SIZE
ROBOT_MOVES = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (-1, -1), (1, -1), (-1, 1)]

def manhattanDistance(pos1, pos2):
    return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])

# Helper function to get best robot move
def getBestRobotMove(robotPosition, targetPosition, obstacles):
    robotX, robotY = robotPosition
    
    # Possible moves that bring the robot closer to the target
    bestMove = None
    bestDistanceToTarget = float('inf')
    
    # Explore all potential moves
    for move in ROBOT_MOVES:
        newRobotX = robotX + move[0]
        newRobotY = robotY + move[1]
        
        # Ensure robot does not move into obstacles or out of bounds
        if (0 <= newRobotX < GRID_SIZE) and (0 <= newRobotY < GRID_SIZE) and (newRobotX, newRobotY) not in obstacles:
            distanceToTarget = manhattanDistance((newRobotX, newRobotY), targetPosition)
            
            # Choose the move that minimizes the distance to the target
            if distanceToTarget < bestDistanceToTarget:
                bestMove = (move[0], move[1])
                bestDistanceToTarget = distanceToTarget

    # Return the best move toward the target, or None if no move is found
    return bestMove
# end getBestRobotMove

# Movement logic for robot
def moveRobot(robotPosition, bullPosition, targetPosition, obstacles):    
    # If robot is not within bull's 5x5 move towards bull
    if manhattanDistance(bullPosition, robotPosition) > 5:
        target = bullPosition
    else:
        target = targetPosition

    
    # Calculate robot's movement strategy by trying to move towards target
    bestMove = getBestRobotMove(robotPosition, target, obstacles)
    if bestMove:
        robotPosition[0] += bestMove[0]
        robotPosition[1] += bestMove[1]
# end moveRobot                 