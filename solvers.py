'''
Several different possible solving algorithms for any given board state
'''
import copy
from framework import *


def brute_force(board):
    '''
    This method will test every possible swap on the board (with no playthrough,
    i.e., only considering the results of the swap itself) and return the pair
    with the highest score

    Inputs:
        board (Board): the board in the state to be tested

    Returns:
        pair (tuple): the pair of coordinates with the highest score
    '''
    # Store the state of the grid when the function is run
    starting_grid = copy.deepcopy(board.grid)
    starting_score = board.score

    # Initialize outputs
    pair = ((),())
    highest = 0

    # Try swapping every element in the j direction:
    for i in range(board.size):
        for j in range(board.size - 1):
            board.swap2_no_replacement((i, j), (i, j + 1))

            # If the score increases, a match was made
            if board.score > starting_score:

                # If this yields a higher score than the current highest,
                # update the outputs accordingly
                if board.score - starting_score > highest:
                    highest = board.score - starting_score
                    pair = ((i, j), (i, j + 1))

                # Clear the board and reset the score
                board.grid = copy.deepcopy(starting_grid)
                board.score = starting_score
                continue

            # Restore the board and continue
            board.grid = copy.deepcopy(starting_grid)
            board.score = starting_score

    # Repeat in the i direction
    for i in range(board.size - 1):
        for j in range(board.size):
            board.swap2_no_replacement((i, j), (i + 1, j))

            if board.score > starting_score:

                if board.score - starting_score > highest:
                    highest = board.score - starting_score
                    pair = ((i, j), (i + 1, j))

                board.grid = copy.deepcopy(starting_grid)
                board.score = starting_score
                continue

            board.grid = copy.deepcopy(starting_grid)
            board.score = starting_score

    # Return the highest pair
    return pair

def empirical(board, loops=1):
    '''
    This method will try every swap on the board with simulated playthrough.
    The optional loops parameter allows this to be done many times, selecting
    the pair that is the highest scorer with the greatest frequency

    Inputs:
        board (Board): the current board state
        loops (int): the number of times to simulate playthrough

    Returns:
        pair (tuple): the highest scoring pair over the given number of loops
    '''
    # Store the pair frequencies in a dictionary
    frequencies = {}

    for i in range(loops):
        # Store the state of the grid when the function is run
        starting_grid = copy.deepcopy(board.grid)
        starting_score = board.score

        # Initialize outputs
        pair = ((),())
        highest = 0

        # Try swapping every element in the j direction:
        for i in range(board.size):
            for j in range(board.size - 1):
                board.swap2((i, j), (i, j + 1))

                # If the score increases, a match was made
                if board.score > starting_score:
                    if board.score - starting_score > highest:
                        highest = board.score - starting_score
                        pair = ((i, j), (i, j + 1))
                    board.grid = copy.deepcopy(starting_grid)
                    board.score = starting_score
                    continue

                # Restore the board and continue
                board.grid = copy.deepcopy(starting_grid)
                board.score = starting_score

        # Repeat in the i direction
        for i in range(board.size - 1):
            for j in range(board.size):
                board.swap2((i, j), (i + 1, j))

                if board.score > starting_score:
                    if board.score - starting_score > highest:
                        highest = board.score - starting_score
                        pair = ((i, j), (i + 1, j))
                    board.grid = copy.deepcopy(starting_grid)
                    board.score = starting_score
                    continue

                board.grid = copy.deepcopy(starting_grid)
                board.score = starting_score

        # Increment the frequency of the pair
        if pair in frequencies:
            frequencies[pair] += 1
        else:
            frequencies[pair] = 1

    # Return the dictionary item with the most tallies
    return max(frequencies, key=frequencies.get)
