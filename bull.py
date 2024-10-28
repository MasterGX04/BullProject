import random
from grid_size import GRID_SIZE
#Possible movements: up, down, left, and right
BULL_MOVES = [(0, 1), (0, -1), (1, 0), (-1, 0)]

def manhattanDistance(pos1, pos2):
    return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1]) 
     
# Determine if the robot is within a 5x5 square centered on the bull
def isWithin5x5Square(bullPosition, robotPosition):
    bullX, bullY = bullPosition 
    robotX, robotY = robotPosition
    
    return (bullX - 2 <= robotX <= bullX + 2) and (bullY - 2 <= robotY <= bullY + 2)

def getBestChargingDirection(bullPosition, robotPosition, obstacles):
    currentDistance = manhattanDistance(bullPosition, robotPosition)
    closestPositions = []
    minDistance = float('inf')
    
    # Iterate over each possible direction
    for move in BULL_MOVES:
        newPosition = bullPosition
        while True:
            # Move one step further in the current direction
            newPosition = (newPosition[0] + move[0], newPosition[1] + move[1])
            
            # Stop if we hit an obstacle
            if newPosition in obstacles:
                break
            
            # Calculate the distance to the robot from this position
            newDistance = manhattanDistance(newPosition, robotPosition)
            
            # Check if this is the closest reachable position so far
            if newDistance < minDistance:
                minDistance = newDistance
                closestPositions = [move]
            elif newDistance == minDistance:
                closestPositions.append(move)
            
            # Stop searching further if we exceed the current minimum distance
            if newDistance >= currentDistance:
                break
    
    # Randomly select one of the closest directions
    return random.choice(closestPositions) if closestPositions else None
# End getBestChargingDirection

def printDirection(direction):
    if direction == (0, 1): 
        print('Bull is charging to the right')
    elif direction == (0, -1):
        print ('Bull is charging to the left')
    elif direction == (1, 0):
        print('Bull is charging to the bottom')
    else:
        print('Bull is charging to the top')
        
#Bull movement logic
def moveBull(bullPosition, robotPosition, obstacles, chargingDirection):
    bullX, bullY = bullPosition
    possibleMoves = []
    if chargingDirection is not None: print(f"Charging direction: {chargingDirection}")
    
    #If robot is within a 5x5 square around bull
    if isWithin5x5Square(bullPosition, robotPosition):
        print(f"Robot is within 5x5 square of bull at {robotPosition} vs bullPos: {bullPosition}")
        if chargingDirection is None:
            possibleMoves = []
            for move in BULL_MOVES:
                chargingDirection = getBestChargingDirection(bullPosition, robotPosition, obstacles)
                printDirection(chargingDirection)
                
        # If charging direction exists, continue in that direction as long as it doesn’t increase the distance    
        if chargingDirection is not None:
            newBullX = bullX + chargingDirection[0]
            newBullY = bullY + chargingDirection[1]
            
            # Check if moving chosen direction is still valid
            if (0 <= newBullX < GRID_SIZE and 0 <= newBullY < GRID_SIZE) and (newBullX, newBullY) not in obstacles:
                # Update bull position to continue charging in the same direction
                bullPosition[0] = newBullX
                bullPosition[1] = newBullY
            else:
                chargingDirection = None
            
    else:    
        #Random move if robot is outside 5x5 area
        chargingDirection = None
        for move in BULL_MOVES:
            newBullX = bullX + move[0]
            newBullY = bullY + move[1]
            #Grid border check and not going to same position as obstacle or robot
            if 0 <= newBullX < GRID_SIZE and 0 <= newBullY < GRID_SIZE and \
                (newBullX, newBullY) != tuple(robotPosition) and (newBullX, newBullY) not in obstacles:
                possibleMoves.append(move)
        if possibleMoves:
            move = random.choice(possibleMoves)
            bullPosition[0] += move[0]
            bullPosition[1] += move[1]
    
    return chargingDirection

# End moveBull