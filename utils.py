import numpy as np
from global_functions import GRID_SIZE

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

def isWithin5x5Square(bullPosition, robotPosition):
    bullX, bullY = bullPosition
    robotX, robotY = robotPosition
    return (bullX - 2 <= robotX <= bullX + 2) and (bullY - 2 <= robotY <= bullY + 2)

def manhattanDistance(pos1, pos2):
    return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])

def placeTarget(grid):
    center_row = int(GRID_SIZE / 2)
    center_col = int(GRID_SIZE / 2)
    grid[center_row][center_col] = 3  # Value for target
    return (center_row, center_col)

def calculateReward(robotPosition, bullPosition, targetPosition):   
    bullToTargetDistance = manhattanDistance(bullPosition, targetPosition)
    robotToBullDistance = manhattanDistance(robotPosition, bullPosition)
    robotToTargetDistance = manhattanDistance(robotPosition, targetPosition)
    
    corralPositions = [
        (targetPosition[0] - 1, targetPosition[1]),
        (targetPosition[0] - 2, targetPosition[1]),
        (targetPosition[0] - 2, targetPosition[1] - 1),
        (targetPosition[0] - 2, targetPosition[1] + 1)
    ]
    
    # print(f'Corral positions: {list(corralPositions)}')
    
     # Encourage the robot to "jump out" to a diagonal position
    diagonalExits = [
        (targetPosition[0] - 2, targetPosition[1] - 1),
        (targetPosition[0] - 2, targetPosition[1] + 1)
    ]
    
    patrolZone = [
        (targetPosition[0] - 2, targetPosition[1] - 2), (targetPosition[0] - 2, targetPosition[1] - 1),
        (targetPosition[0] - 2, targetPosition[1]), (targetPosition[0] - 2, targetPosition[1] + 1),
        (targetPosition[0] - 2, targetPosition[1] + 2), (targetPosition[0] - 1, targetPosition[1] + 2),
        (targetPosition[0], targetPosition[1] + 2), (targetPosition[0] + 1, targetPosition[1] + 2),
        (targetPosition[0] + 2, targetPosition[1] + 2), (targetPosition[0] + 2, targetPosition[1] + 1),
        (targetPosition[0] + 2, targetPosition[1]), (targetPosition[0] + 2, targetPosition[1] - 1),
        (targetPosition[0] + 2, targetPosition[1] - 2), (targetPosition[0] + 1, targetPosition[1] - 2),
        (targetPosition[0], targetPosition[1] - 2), (targetPosition[0] - 1, targetPosition[1] - 2)
    ]
                
    reward = 0
    if bullPosition == targetPosition:
        reward += 100
    else:
        reward += max(0, 30 - bullToTargetDistance)
        
        if isWithin5x5Square(targetPosition, bullPosition):
            reward -= 8 * robotToTargetDistance
        
        if isWithin5x5Square(bullPosition, robotPosition):
            reward += max(0, 10 - robotToBullDistance)
            reward += 2 * max(0, 20 - robotToTargetDistance)
            if robotPosition in corralPositions:
            # Reward for being in the corral if the bull is close
                reward += 25
                # Reward diagonal escape options to lure the bull in
                if robotPosition in diagonalExits:
                    reward += 15
            elif targetPosition[1] - 1 <= robotPosition[1] <= targetPosition[1] + 1 and robotPosition[0] < targetPosition[0]:
                # Reward if the robot is approaching from the top direction
                reward += 15
            else:
                # Penalize if trying to enter from an invalid side
                reward -= 15
            if robotPosition in patrolZone:
                reward += 15  # Moderate reward for staying within patrol zone

                # Additional reward for moving sequentially through patrol zone (looping effect)
                adjacentPatrolPositions = [
                    (robotPosition[0] - 1, robotPosition[1]),
                    (robotPosition[0] + 1, robotPosition[1]),
                    (robotPosition[0], robotPosition[1] - 1),
                    (robotPosition[0], robotPosition[1] + 1)
                ]
                if any(pos in patrolZone for pos in adjacentPatrolPositions):
                    reward += 5
        else:
            reward -= 3 * (robotToBullDistance)
        
        #if bullToTargetDistance <= 2 and robotToTargetDistance <= 2:
    return reward
    
