import numpy as np

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
