'''
A back end framework that allows the game to run in a basic text format.
The board class is defined, as well as helper functions for swapping
items, checking for matches, and calculating scores.
'''

import random


class board:
    '''
    This allows for the generation of board objects. Boards are defined by the convention
    self.grid[i][j], where directions are:
     → i
    ↓
    j

    After initializing, boards can swap items and check for matches
     '''
    def __init__(self, size=5, colors=["r", "g", "b", "y"]):
        '''
        Initialize the board by randomly populating it and then clearing any matches
        that may appear
        
        Inputs:
            size (int, optional): a dimension of the square board
            colors (list of strings, optional): the colors with which to populate the board

        Returns:
            None
        '''
        # Initialize parameters
        self.size = size
        self.colors = colors
        self.score = 0

        # Populate the board randomly
        self.grid = [[random.choice(colors) for i in range(size)] for j in range(size)]

        # Clear matches and reset the score
        self.match()
        self.score = 0
    
    def __repr__(self):
        '''
        A string representation of the board which outputs it as a grid with the current score
        
        Inputs:
            None
        
        Returns:
            None
        '''
        for i in range(self.size):
            row = ""
            for j in range(self.size):
                row += str(self.grid[j][i]) + " "
            print(row)
        return "Score: " + str(self.score)

    def match(self):
        '''
        Checks every row and column of the board for matches, scores them, and refills the board
        
        Inputs:
            None
        
        Returns:
            None
        '''
        # Run until all matches are cleared because more might show up as the pieces shift
        while True:
            # Initialize list of coordinates to remove
            coords = []

            # Select columns
            for i in range(self.size):
                column = self.grid[i]

                # Check for matches
                if group_chk(column) is not None:
                    grps = group_chk(column).split("s")

                    # Score each match based on how many pieces it contains
                    for j in grps[:-1]:
                        self.score += 2 * len(j) - 5

                        # Add each coordinate to the list to clear
                        listed = [k for k in j]
                        for k in listed:
                            coords.append((i, k))
        
            
            # Repeat for rows
            for i in range(self.size):
                row = [self.grid[j][i] for j in range(self.size)]

                if group_chk(row) is not None:
                    grps = group_chk(row).split("s")

                    for k in grps[:-1]:
                        self.score += 2 * len(k) - 5

                        listed = [l for l in k]
                        for l in listed:
                            # If two matches intersect, add additional points
                            if (l, i) in coords:
                                self.score += 2
                                continue
                            else:
                                coords.append((l, i))
            
            # Stop the infinite loop if no matches were found
            if coords == []:
                break

            # Mark all coordinates to remove from the board
            for i in coords:
                self.grid[int(i[0])][int(i[1])] = 0

            # Pop each marked item out of the board
            for i in range(self.size):
                j = 0
                while True:
                    try:
                        if self.grid[i][j] == 0:
                            self.grid[i].pop(j)
                        else:
                            j += 1
                    except IndexError:
                        break

            # Refill columns from the top with random pieces
            for i in coords:  
                self.grid[int(i[0])].insert(0, random.choice(self.colors))
    
    def swap(self, pos1, pos2):
        '''
        Swap two items in the grid and check for matches

        Inputs:
            pos1 (iterable, ints): the coordinate of the first item to swap
            pos1 (iterable, ints): the coordinate of the second item to swap

        Returns:
            None
        '''
        # Swap the items
        item1 = self.grid[pos1[0]][pos1[1]]
        item2 = self.grid[pos2[0]][pos2[1]]

        self.grid[pos1[0]][pos1[1]] = item2
        self.grid[pos2[0]][pos2[1]] = item1
        
        # Check for matches
        self.match()
    

def group_chk(row):
    '''
    A helper function that identifies groups of the same item in a list
    
    Inputs:
        row (iterable): the list of items in which to find groups
        
    Returns:
        positions (string): a string containing each group of matching indices.
            The groups are separated by the spacer character 's'. If no matches
            are found, returns None.
    '''
    # Use two pointers
    i = 0
    j = 0

    # Initialize positions of groups
    positions = []

    # Lengthen input by one to be able to check the end without causing an index error
    row.append("random garbage")

    # Check for matches
    while j < len(row):
        # Count how many consecutive items are the same
        if row[i] == row[j]:
            j += 1

        # If a group of three or more is found, append its indices to positions
        elif j - i >= 3:
            for k in range(i, j):
                positions.append(str(k))
            
            # Append a spacer character to positions
            positions.append("s")

            # Continue moving forward
            i = j

        else:
            # Move forward
            i = j

    # Return none if no groups are found
    if positions == []:
        return None

    # Return output as a string
    return ''.join(positions)
