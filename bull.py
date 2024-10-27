import random
from grid_size import GRID_SIZE
#Possible movements: up, down, left, and right
BULL_MOVES = [(0, 1), (0, -1), (1, 0), (-1, 0)]

def manhattanDistance(pos1, pos2):
    return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1]) 
        
# End computeTStar
#Bull movement logic
def moveBull(bullPosition, robotPosition, obstacles, corralPositions):
    bullX, bullY = bullPosition
    possibleMoves = []
    global corralPos
    corralPos = corralPositions
    
    #If robot is within a 5x5 square around bull
    if manhattanDistance(bullPosition, robotPosition) <= 5:
        for move in BULL_MOVES:
            newBullX = bullX + move[0]
            newBullY = bullY + move[1]
            newPosition = [newBullX, newBullY]
            #Ensure bull moves to robot
            if (0 <= newBullX < GRID_SIZE and 0 <= newBullY < GRID_SIZE) and (newBullX, newBullY) not in obstacles:
               # Check if this move maintains or decreases the distance to the robot
                if manhattanDistance(newPosition, robotPosition) <= manhattanDistance(bullPosition, robotPosition):
                    possibleMoves.append(move)
        #end bull move check
        #Randomly choose valid move for bull
        if possibleMoves:
            chosenMove = random.choice(possibleMoves)
            bullPosition[0] += chosenMove[0]
            bullPosition[1] += chosenMove[1]
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