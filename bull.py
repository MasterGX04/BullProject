import random
from grid_size import GRID_SIZE
#Possible movements: up, down, left, and right
BULL_MOVES = [(0, 1), (0, -1), (1, 0), (-1, 0)]
from robot import getBestRobotMove

def manhattanDistance(pos1, pos2):
    return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])

# Cache results for computed states to avoid redundant calculations
tStarCache = []

# Recursive function to compute T* for given bull and robot position
def computeTStar(bullPosition, robotPosition, obstacles):
    # Checks if result is cached
    state = (bullPosition[0], bullPosition[1], robotPosition[0], robotPosition[1])
    if state in tStarCache:
        return tStarCache[state]
    
    bullX, bullY = bullPosition
    possibleMoves = []
    
    # Explore all possible moves to minimize distance to target
    for move in BULL_MOVES:
        newBullX = bullX + move[0]
        newBullY = bullY + move[1]
        newPosition = [newBullX, newBullY]
        
        # Check if move is within grid 
        if (0 <= newBullX < 13 and 0 <= newBullY < 13) and (newBullX, newBullY) not in obstacles:
            bestRobotMove = getBestRobotMove(robotPosition, newPosition, obstacles)
            nextRobotPosition = [robotPosition[0] + bestRobotMove[0], robotPosition[1] + bestRobotMove[1]]
                            
            # Recursively calcularte T* for next positions
            tStarValue = 1 + computeTStar(newPosition, nextRobotPosition, obstacles)
            possibleMoves.append(tStarValue)
        
    # Find min T* from all possible moves
    tStarCache[state] = min(possibleMoves) if possibleMoves else float('inf')
    return tStarCache[state]
                     
        
# End computeTStar
#Bull movement logic
def moveBull(bullPosition, robotPosition, obstacles):
    bullX, bullY = bullPosition
    robotX, robotY = robotPosition
    
    possibleMoves = []
    #If robot is within a 5x5 square around bull
    if manhattanDistance(bullPosition, robotPosition) <= 5:
        for move in BULL_MOVES:
            newBullX = bullX + move[0]
            newBullY = bullY + move[1]
            newPosition = [newBullX, newBullY]
            #Ensure bull moves to robot
            if (0 <= newBullX < 13 and 0 <= newBullY < 13) and (newBullX, newBullY) not in obstacles:
                # Compute T* for the next position
                tStarValue = computeTStar(newPosition, robotPosition, obstacles)
                possibleMoves.append((move, tStarValue))
        #end bull move check
        #Randomly choose valid move for bull
        if possibleMoves:
            bestMove = min(possibleMoves, key=lambda x: x[1])[0]
            bullPosition[0] += bestMove[0]
            bullPosition[1] += bestMove[1]
    else:
        #Random move if robot is outside 5x5 area
        for move in BULL_MOVES:
            newBullX = bullX + move[0]
            newBullY = bullY + move[1]
            #Grid border check and not going to same position as obstacle or robot
            if 0 <= newBullX < GRID_SIZE and 0 <= newBullY < GRID_SIZE and (newBullX, newBullY) != tuple(robotPosition) and (newBullX, newBullY) not in obstacles:
                possibleMoves.append(move)
        if possibleMoves:
            move = random.choice(possibleMoves)
            bullPosition[0] += move[0]
            bullPosition[1] += move[1]
# End moveBull