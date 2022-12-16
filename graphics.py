'''
The script that will run the GUI for the game in Pygame
'''
import sys
import copy
import random
import pygame

from framework import group_chk


class Jewel(pygame.sprite.Sprite):
    '''
    A class to represent jewels on the board as game objects for
    easy display and animation (subclass of the built-in Sprite class)
    '''
    def __init__(self, color, center=(0, 0)):
        '''
        Initialize the jewel at a certain position on the board

        Inputs:
            color (str): "r", "g", "b", or "y" for red, green,
                blue, or yellow
            center (tuple): the coordinates (in pixels) of the
                center of the jewel
        Returns:
            None
        '''
        # Initialize as a pygame sprite
        pygame.sprite.Sprite.__init__(self)

        # Update the color, image, and position
        self.color = color
        self.image = pygame.image.load(self.select_img_file())
        self.rect = self.image.get_rect()
        self.rect.center = center

    def select_img_file(self):
        '''
        Convert the single character representation
        of each color to its respective image file

        Inputs:
            None

        Returns:
            path (str): the path of the image specified
                by self.color
        '''
        files = {
            "r": "jewels/red.png",
            "b": "jewels/blue.png",
            "g": "jewels/green.png",
            "y": "jewels/yellow.png"
        }
        return files[self.color]



class Board(pygame.sprite.RenderUpdates):
    '''
    This allows for the generation of board objects. Boards are defined by the convention
    self.grid[i][j], where directions are:
     → i
    ↓
    j
    (indexed starting at 0)

    After initializing, boards can swap items and check for matches

    This version of the board class is a subclass of the pygame RenderUpdates class,
    which allows for easy display of all game objects
     '''
    def __init__(self, size=7, colors=["r", "g", "b", "y"]):
        '''
        Initialize the board by randomly populating it and then clearing any matches
        that may appear

        Inputs:
            size (int, optional): a dimension of the square board
            colors (list of strings, optional): the colors with which to populate the board

        Returns:
            None
        '''
        # Initialize the RenderUpdates class
        pygame.sprite.RenderUpdates.__init__(self)

        # Initialize parameters
        self.size = size
        self.colors = colors
        self.score = 0

        # Populate the board randomly as a 2D list of nested lists
        self.grid = [[random.choice(colors) for i in range(size)] for j in range(size)]

        # Clear matches and reset the score
        self.match()
        self.score = 0

        # If no matches exist, shuffle until they do
        while not self.matches_exist():
            self.shuffle()
            self.score = 0

        # Update the board and blit everything to the screen
        self.update()

    def update(self):
        '''
        A function which clears the current board and blits everything to the screen

        Inputs:
            None

        Returns:
            None
        '''
        # Empty the board
        self.empty()

        # Refill the board with jewels from the grid
        for i in range(self.size):
            for j in range(self.size):
                self.add(Jewel(color=self.grid[j][i], center=(24 + 50 * j, 24 + 50 * i)))

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
                        for k in list(j):
                            coords.append((i, k))


            # Repeat for rows
            for i in range(self.size):
                row = [self.grid[j][i] for j in range(self.size)]

                if group_chk(row) is not None:
                    grps = group_chk(row).split("s")

                    for k in grps[:-1]:
                        self.score += 2 * len(k) - 5

                        for l in list(k):
                            # If two matches intersect, add additional points
                            if (l, i) in coords:
                                self.score += 2
                                continue

                            coords.append((l, i))

            # Stop the infinite loop if no matches were found
            if not coords:
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

        # Update the board
        self.update()

    def swap(self, pos1, pos2):
        '''
        Swap two items in the grid and check for matches

        Inputs:
            pos1 (tuple): the coordinate of the first item to swap
            pos1 (tuple): the coordinate of the second item to swap

        Returns:
            None
        '''
        # Remember the starting score
        starting_score = self.score

        # Swap the items
        item1 = self.grid[pos1[0]][pos1[1]]
        item2 = self.grid[pos2[0]][pos2[1]]

        self.grid[pos1[0]][pos1[1]] = item2
        self.grid[pos2[0]][pos2[1]] = item1

        # Check for matches
        self.match()

        # If the swap was useless, swap them back
        if self.score == starting_score:
            self.grid[pos1[0]][pos1[1]] = item1
            self.grid[pos2[0]][pos2[1]] = item2

        # If the swap was valid
        else:
            # If no matches exist, shuffle until they do
            while not self.matches_exist():
                self.shuffle()

        # Update the board
        self.update()

    def swap2(self, pos1, pos2):
        '''
        Swap two items in the grid and check for matches. This version of the function does NOT use
        the matches_exist() function in order to avoid infinite looping

        Inputs:
            pos1 (tuple): the coordinate of the first item to swap
            pos1 (tuple): the coordinate of the second item to swap

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

        self.update()

    def shuffle(self):
        '''
        Randomly shuffle the items on the board and check for matches.

        Inputs:
            None

        Returns:
            None
        '''
        # Store all current board items
        items = []
        for i in range(self.size):
            for j in range(self.size):
                items.append(self.grid[i][j])

        # Randomize the items and place them back on the board
        random.shuffle(items)
        for i in range(self.size):
            for j in range(self.size):
                self.grid[i][j] = items.pop()

        # Clear any matches that show up
        self.match()

        # Update the board
        self.update()

    def matches_exist(self):
        '''
        Scans the board and tries every possible switch to determine if any
        matches are possible.

        Inputs:
            None

        Returns:
            bool: True if matches are possible, False if not
        '''
        # Store the state of the grid when the function is run
        starting_grid = copy.deepcopy(self.grid)
        starting_score = self.score

        # Try swapping every element in the j direction:
        for i in range(self.size):
            for j in range(self.size - 1):
                self.swap2((i, j), (i, j + 1))

                # If the score increases, a match was made
                if self.score > starting_score:
                    self.grid = copy.deepcopy(starting_grid)
                    self.score = starting_score
                    return True

                # Restore the board and continue
                self.grid = copy.deepcopy(starting_grid)
                self.score = starting_score

        # Repeat in the i direction
        for i in range(self.size - 1):
            for j in range(self.size):
                self.swap2((i, j), (i + 1, j))

                if self.score > starting_score:
                    self.grid = copy.deepcopy(starting_grid)
                    self.score = starting_score
                    return True

                self.grid = copy.deepcopy(starting_grid)
                self.score = starting_score

        # If nothing was found, return False
        return False


def main(turns=10):
    '''
    The script that will run the game

    Inputs:
        turns (int): the number of turns to play
        size (int): the size of the board to play on (between 5 and 10 recommended)

    Returns:
        None
    '''
    # Initialize a board object
    board = Board()

    # Initialize the display based on the board size selected
    pygame.init()
    pygame.display.set_caption("Bejeweled But Worse")
    dimensions = board.size * 50, board.size * 50 + 40
    screen = pygame.display.set_mode(dimensions)

    # Initialize a font for displaying the score
    font = pygame.font.Font('freesansbold.ttf', 32)

    # Initialize the mouse position and the current number of turns
    pos = None
    count = 0

    # Run the game
    while True:
        # If the number of turns has been met, show the game over screen
        if count == turns:
            # Quit when the quit button is pressed
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

            # Clear the screen
            screen.fill((0, 0, 0))

            # Blit the game over message to the screen, along with the board
            game_over = font.render("Game Over!", True, (250, 250, 250))
            over_rect = game_over.get_rect()
            over_rect.center = (int(50 * board.size / 2), int(50 * board.size / 2))
            screen.blit(game_over, over_rect)
            screen.blit(score_text, score_rect)

            # Flip the display
            pygame.display.flip()

        # If there are turns still to be played
        else:
            # Exit the game if a quit event has been queued
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

                # When the mouse is pressed, get its position
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    # Map the i coordinate to a jewel
                    i = 0
                    x_click = event.__dict__["pos"][0]
                    x_bound = 50
                    while x_click > x_bound:
                        i += 1
                        x_bound += 50

                    # Map the j coordinate to a jewel
                    j = 0
                    y_click = event.__dict__["pos"][1]
                    y_bound = 50
                    while y_click > y_bound:
                        j += 1
                        y_bound += 50

                    # If no jewel has been clicked yet, initialize this jewel
                    if pos is None:
                        pos = (i, j)

                    # If a first jewel has been clicked, check if this jewel is a neighbor
                    else:
                        if (i, j) in [(pos[0] + 1, pos[1]), (pos[0] - 1, pos[1]),
                            (pos[0], pos[1] + 1), (pos[0], pos[1] - 1)]:

                            # Swap the two if yes
                            board.swap(pos, (i, j))

                            # Clear the current position and increment turns by one
                            pos = None
                            count += 1

                        else:
                            # If not a neighbor, update position
                            pos = (i, j)

            # Clear the screen
            screen.fill((0, 0, 0))

            # Redraw the background
            board.draw(screen)

            # Display the score at the bottom left
            score_text = font.render("Score: " + str(board.score), True, (250, 250, 250))
            score_rect = score_text.get_rect()
            score_rect.top = 5 + 50 * board.size
            screen.blit(score_text, score_rect)

            # Display the number of turns at the bottom right
            turns_text = font.render("Turns: " + str(turns - count), True, (250, 250, 250))
            turns_rect = score_text.get_rect()
            turns_rect.top = 5 + 50 * board.size
            turns_rect.right = 50 * board.size - 25
            screen.blit(turns_text, turns_rect)

            # Refresh the display
            pygame.display.flip()
