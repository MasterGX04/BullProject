import random
from global_functions import GRID_SIZE

# Possible movements: up, down, left, and right
BULL_MOVES = [(0, 1), (0, -1), (1, 0), (-1, 0)]


def manhattanDistance(pos1, pos2):
    return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])


# Determine if the robot is within a 5x5 square centered on the bull
def isWithin5x5Square(bullPosition, robotPosition):
    bullX, bullY = bullPosition
    robotX, robotY = robotPosition

    return (bullX - 2 <= robotX <= bullX + 2) and (bullY - 2 <= robotY <= bullY + 2)


# Bull movement logic
def moveBull(bullPosition, robotPosition, obstacles, corralPosition):
    bullX, bullY = list(bullPosition)  # Convert tuple to list for mutation
    possibleMoves = []
    mandatoryMove = None
    
    # print('Bull corralPosition:', corralPosition)
    
    # If robot is within a 5x5 square around bull
    if isWithin5x5Square(bullPosition, robotPosition):
        if bullPosition == (corralPosition[0] + 1, corralPosition[1]):
            bullX += 1
            return (bullX, bullY)
        
        for move in BULL_MOVES:
            newBullX = bullX + move[0]
            newBullY = bullY + move[1]
            newPosition = [newBullX, newBullY]
            # Ensure bull moves towards the robot
            if (0 <= newBullX < GRID_SIZE and 0 <= newBullY < GRID_SIZE) and \
               (newBullX, newBullY) not in obstacles and newPosition != tuple(robotPosition):
                # Check if this move maintains or decreases the distance to the robot
                if manhattanDistance(newPosition, robotPosition) <= manhattanDistance(bullPosition, robotPosition):
                    possibleMoves.append(move)
                if bullPosition == corralPosition:
                    if newPosition != tuple(robotPosition):
                        possibleMoves.append((1, 0))
        # Randomly choose valid move for bull
        if possibleMoves:
            chosenMove = random.choice(possibleMoves)
            bullX += chosenMove[0]
            bullY += chosenMove[1]
    else:
        # Random move if robot is outside 5x5 area
        for move in BULL_MOVES:
            newBullX = bullX + move[0]
            newBullY = bullY + move[1]
            if (0 <= newBullX < GRID_SIZE and 0 <= newBullY < GRID_SIZE and
                    (newBullX, newBullY) != tuple(robotPosition) and
                    (newBullX, newBullY) not in obstacles):
                possibleMoves.append(move)
        if possibleMoves:
            move = random.choice(possibleMoves)
            bullX += move[0]
            bullY += move[1]

    return (bullX, bullY)  # Return the new position as a tuple
