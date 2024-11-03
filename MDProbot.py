from grid_size import GRID_SIZE
from utils import isWithin5x5Square, placeWallsAroundTarget, manhattanDistance, placeTarget
import numpy as np
import random
from bull import moveBull

ACTIONS = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (-1, -1), (1, -1), (-1, 1)]  # Robot Moves

class MDPGrid:
    
    """
    A class representing a Markov Decision Process (MDP) grid environment 
    where a robot tries to lure a bull into a corral while avoiding collisions.
    """
    
    def __init__(self, grid_size, target_row, target_col):
        
        """
        Initializes the MDPGrid with the specified grid size and target position.
        
        Parameters:
            grid_size (int): The size of the grid (width and height).
            target_row (int): The row index for the center of the corral.
            target_col (int): The column index for the center of the corral.
        """
        self.grid_size = grid_size
        self.grid = np.zeros((grid_size, grid_size), dtype=int)
        
        # Set up target and corral walls
        self.target_center = placeTarget(self.grid)  # Center of the target
        self.walls, self.corral = placeWallsAroundTarget(self.grid, target_row, target_col)
        
        self.previous_distance_to_bull = None

        
    def is_valid_state(self, state):
        """
        Checks if the given state is valid (i.e., not a wall).

        Parameters:
            state (tuple): A tuple representing the (row, column) of the state.

        Returns:
            bool: True if the state is valid, False otherwise.
        """
        row, col = state
        return (0 <= row < self.grid_size and 
                0 <= col < self.grid_size and 
                self.grid[row, col] == 0)

    def get_possible_actions(self, state, bull_position):
        """
        Parameters:
            state (tuple): The current position of the robot (row, column).
            bull_position (tuple): The current position of the bull (row, column).

        Returns:
            list: A list of valid actions represented as (delta_row, delta_col).
        """
        actions = []
        for dr, dc in ACTIONS:
            new_state = (state[0] + dr, state[1] + dc)
            # Check if the new state is valid and not the same as the bull's position
            if self.is_valid_state(new_state) and new_state != bull_position:
                actions.append((dr, dc))  # Store deltas for easier movement
        return actions

    def reward_function(self, robot_position, bull_position):
        """
        Calculates the reward based on the current positions of the robot and bull.

        Parameters:
            robot_position (tuple): The current position of the robot (row, column).
            bull_position (tuple): The current position of the bull (row, column).

        Returns:
            float: The calculated reward.
        """
        reward = 0
        if bull_position == self.target_center:
            reward += 10
            return reward
        # Proximity reward if bull is close to corral center
        corral_distance = manhattanDistance(bull_position, self.target_center)
        if corral_distance <= 2:
            reward += 5
        # Reward or penalty based on robot's proximity to bull
        if self.previous_distance_to_bull is not None:
            distance_to_bull = manhattanDistance(robot_position, bull_position)
            reward += 0.5 if distance_to_bull < self.previous_distance_to_bull else -0.1
        self.previous_distance_to_bull = manhattanDistance(robot_position, bull_position)
        return reward

    def transition(self, robot_position, bull_position):
        """
        Calculates the next state based on the robot's movement and the bull's response.

        Parameters:
            robot_position (tuple): The current position of the robot (row, column).
            bull_position (tuple): The current position of the bull (row, column).

        Returns:
            tuple: The new positions of the robot and bull as (robot_position, bull_position).
        """
        """Manage state-based transition logic."""
        # Choose target based on proximity to bull
        if isWithin5x5Square(robot_position, bull_position):
            target_position = self.target_center  # Move towards corral
        else:
            target_position = bull_position  # Move towards bull

        # Get possible actions for robot
        possible_actions = self.get_possible_actions(robot_position, bull_position)
        
        # Choose action moving the robot closer to target position (bull or corral)
        if possible_actions:
            chosen_action = min(
                possible_actions,
                key=lambda action: manhattanDistance(
                    (robot_position[0] + action[0], robot_position[1] + action[1]), target_position
                )
            )
            chosen_robot_position = (robot_position[0] + chosen_action[0], robot_position[1] + chosen_action[1])
        else:
            chosen_robot_position = robot_position  # No valid moves, stay in place

        # Move bull based on robot's new position
        new_bull_position = moveBull(bull_position, chosen_robot_position, self.walls, {self.target_center})

        # Calculate reward
        reward = self.reward_function(chosen_robot_position, new_bull_position)
        return chosen_robot_position, new_bull_position
    
    def transition_model(self, robot_position, action, next_state):
        """
        Defines the transition model. Returns 1 if the action leads to the next state, else 0.

        Parameters:
            robot_position (tuple): The current position of the robot (row, column).
            action (tuple): The action taken (delta_row, delta_col).
            next_state (tuple): The next state to check (row, column).

        Returns:
            int: 1 if the action leads to the next state, 0 otherwise.
        """
        new_robot_position = (robot_position[0] + action[0], robot_position[1] + action[1])
        return 1 if new_robot_position == next_state else 0

def value_iteration(self, gamma=0.9, epsilon=1e-6):
    """
    Performs value iteration to find the optimal policy and value function.

    Parameters:
        gamma (float): Discount factor for future rewards (default is 0.9).
        epsilon (float): Convergence threshold (default is 1e-6).

    Returns:
        tuple: A tuple containing the optimal policy and the value function.
    """
    # Generate all valid (robot_position, bull_position) states
    states = [((r, c), (b_r, b_c)) for r in range(self.grid_size) for c in range(self.grid_size) 
              for b_r in range(self.grid_size) for b_c in range(self.grid_size)
              if self.is_valid_state((r, c)) and self.is_valid_state((b_r, b_c))]

    # Initialize the value function to zero for all states
    V = {s: 0 for s in states}

    while True:
        delta = 0
        for s in states:
            robot_position, bull_position = s
            v = V[s]

            # Compute expected values for each action and find the max
            max_action_value = float('-inf')
            for a in self.get_possible_actions(robot_position, bull_position):
                action_value = sum(
                    self.transition_model(robot_position, a, (robot_position[0] + a[0], robot_position[1] + a[1])) *
                    (self.reward_function(robot_position, bull_position) + gamma * V.get((robot_position[0] + a[0], robot_position[1] + a[1]), 0))
                    for a in ACTIONS
                )
                max_action_value = max(max_action_value, action_value)
            
            # Update the value function and delta for convergence check
            V[s] = max_action_value
            delta = max(delta, abs(v - V[s]))

        # Check for convergence
        if delta < epsilon:
            break
    
    # Extract optimal policy
    policy = {}
    for s in states:
        robot_position, bull_position = s
        # Find the action that maximizes the expected value for each state
        policy[s] = max(
            self.get_possible_actions(robot_position, bull_position), 
            key=lambda a: sum(
                self.transition_model(robot_position, a, (robot_position[0] + a[0], robot_position[1] + a[1])) *
                (self.reward_function(robot_position, bull_position) + gamma * V.get((robot_position[0] + a[0], robot_position[1] + a[1]), 0))
                for a in ACTIONS
            )
        )
    return policy, V

