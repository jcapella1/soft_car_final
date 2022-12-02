import copy
from framework import Board, group_chk

def brute_force(board):
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

    # Return highest pair
    return pair

def empirical(board, loops=1):
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

    return max(frequencies, key=frequencies.get)

