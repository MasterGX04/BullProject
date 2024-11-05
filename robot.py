from global_functions import GRID_SIZE, ROBOT_MOVES, BULL_MOVES, manhattanDistance
from bull import isWithin5x5Square


# Recursive function to compute T* for given bull and robot position
def value_iteration(grid_size, max_iterations, threshold, corralPositions, corralWalls):
    T_star = {}
    policy = {}

    # Initialize values
    for x_B in range(grid_size):
        for y_B in range(grid_size):
            pos_B = (x_B, y_B)
            for x_R in range(grid_size):
                for y_R in range(grid_size):
                    pos_R = (x_R, y_R)
                    if pos_B == corralPositions:  # Terminal state
                        T_star[(pos_B, pos_R)] = 0
                    else:
                        T_star[(pos_B, pos_R)] = 1000  # Start with infinity

    for _ in range(max_iterations):
        max_change = 0
        for x_B in range(grid_size):
            for y_B in range(grid_size):
                pos_B = (x_B, y_B)
                for x_R in range(grid_size):
                    for y_R in range(grid_size):
                        pos_R = (x_R, y_R)
                        if pos_B != pos_R and pos_B != corralPositions and pos_B not in corralWalls and pos_R not in corralWalls:  # Cannot be in the same position
                            # Calculate expected value from the current state
                            new_action, new_value = calculate_expected_value(pos_B, pos_R, T_star, corralWalls)
                            max_change = max(max_change, abs(T_star[(pos_B, pos_R)] - new_value))
                            T_star[(pos_B, pos_R)] = new_value
                            policy[(pos_B, pos_R)] = new_action

        # Stop if the values converge
        if max_change < threshold:
            break

    return T_star, policy


def calculate_expected_value(pos_B, pos_R, T_star, corralWalls):
    """
    Use to calculate the T_star and policy at a given state by using formula T_star = 1 + E[T_star(action)]
    Parameters:
    pos_B = position of Bull
    pos_R = position of Robot
    T_star = dictionary of all T_star values for each state
    corralWalls = set of all the corral wall positions
    Returns:
    The best action and T_star value at the given state
    """
    best_action = None
    best_value = float('inf')

    # computes all potential
    for move in ROBOT_MOVES:
        Ts = 1
        new_R = (pos_R[0] + move[0], pos_R[1] + move[1])
        if is_valid_move(new_R, corralWalls) and new_R != pos_B:
            if isWithin5x5Square(pos_B, new_R):
                bull_moves = get_bull_moves_toward_robot(pos_B, new_R, corralWalls)
            else:
                bull_moves = get_random_bull_moves(pos_B, corralWalls)

            num_moves = len(bull_moves)
            if num_moves > 0:
                for new_B in bull_moves:
                    Ts += (1 / num_moves) * (T_star[(new_B, new_R)])
            else:
                Ts += T_star[(pos_B, new_R)]

            if Ts < best_value:
                best_value = Ts
                best_action = new_R

    return best_action, best_value


def get_bull_moves_toward_robot(pos_B, pos_R, corralWalls):
    moves = []
    # Calculate potential moves for the bull that decrease Manhattan distance to the robot
    for move in BULL_MOVES:
            new_B = (pos_B[0] + move[0], pos_B[1] + move[1])
            if is_valid_move(new_B, corralWalls) and (new_B != pos_R):
                # Check that it moves closer or stays the same distance to the robot
                if manhattanDistance(new_B, pos_R) < manhattanDistance(pos_B, pos_R):
                    moves.append(new_B)
    return moves


def get_random_bull_moves(pos_B, corralWalls):
    moves = []
    # Add logic to return all valid random moves for the bull
    for move in BULL_MOVES:
            new_B = (pos_B[0] + move[0], pos_B[1] + move[1])
            if is_valid_move(new_B, corralWalls):
                moves.append(new_B)
    return moves


def is_valid_move(pos, corralWalls):
    # Check if the move is within the grid and does not collide with walls/obstacles
    return 0 <= pos[0] < GRID_SIZE and 0 <= pos[1] < GRID_SIZE and pos not in corralWalls


def extract_policy(T_star, corralWalls):
    policy = {}
    for (pos_B, pos_R), value in T_star.items():
        best_action = None
        best_value = float('inf')

        for move in ROBOT_MOVES:
            newRobotX = pos_R[0] + move[0]
            newRobotY = pos_R[1] + move[1]
            new_pos_R = (newRobotX, newRobotY)
            if is_valid_move(new_pos_R) and new_pos_R not in corralWalls and new_pos_R != pos_B:
                expected_value = calculate_expected_value(pos_B, new_pos_R, T_star, True)

                if expected_value > best_value:
                    best_value = expected_value
                    best_action = new_pos_R

        policy[(pos_B, pos_R)] = best_action
    return policy


# Movement logic for robot
def moveRobot(robotPosition, bullPosition, policy):

    pos = policy[(tuple(bullPosition), tuple(robotPosition))]
    #print(pos)
    robotPosition[0] = pos[0]
    robotPosition[1] = pos[1]