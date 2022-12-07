'''
The script that will run the GUI for the game in Pygame
'''
import sys
import pygame
from framework import *


class Jewel:
    '''
    A class to represent jewels on the board as game objects for
    easy display and animation
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
        self.color = color
        self.img_file = self.select_img_file()
        self.jewel = pygame.image.load(self.img_file)
        self.rect = self.jewel.get_rect()
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

    def populate(self):
        '''
        Blits the jewel to the pygame display. This requires the
        pygame display to exist as a global variable named "screen"

        Inputs:
            None

        Returns:
            None
        '''
        screen.blit(self.jewel, self.rect)

if __name__ == "__main__":
    # Initialize a board object
    board = Board(size=10)

    # Initialize the display based on the board size selected
    pygame.init()
    dimensions = board.size * 50, board.size * 50
    screen = pygame.display.set_mode(dimensions)

    # Initialize a 2D nested list structure to store game objects
    game_objects = [[0 for i in range(board.size)] for j in range(board.size)]

    # Populate the list with jewel objects from the board grid
    y = 24
    for i in range(board.size):
        x = 24
        for j in range(board.size):
            game_objects[j][i] = Jewel(color=board.grid[j][i], center=(x, y))
            x += 50
        y += 50

    # Display the objects
    while True:
        # Exit the game if a quit event has been queued
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        # Populate the board from the list of game objects
        for i in range(board.size):
            for j in range(board.size):
                game_objects[j][i].populate()

        # Refresh the display
        pygame.display.flip()
    