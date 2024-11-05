GRID_SIZE = 13
ROBOT_MOVES = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (-1, -1), (1, -1), (-1, 1)]

# Possible movements: up, down, left, and right
BULL_MOVES = [(0, 1), (0, -1), (1, 0), (-1, 0)]

def manhattanDistance(pos1, pos2):
    """
    This calculates the manhattanDistances given 2 positions 
    """
    return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])