# Bejeweled (But Worse)
Software Carpentry Final Project - Jonah Capella

This repository contains the necessary files to run a version of Bejeweled written in Python, as well as a collection of solvers that were tested for performance against human data and one another

## Dependencies

If it is not already installed, use the package manager [pip](https://pip.pypa.io/en/stable/) to intall PyGame.

```bash
pip install pygame
```

## Usage

After cloning the repository, navigate to the project directory and run game.py
```bash
python3 game.py
```
The game will run with the default parameters of 10 turns and a board size of 7x7. These can be easily changed by editing the game.py file. It is recommended that the size of the board is between 5x5 and 10x10 for optimum performance.

Accessing the simulations.ipynb notebook will show the performance of three different solver types compared to human performance.

## Technologies Used
- Pygame
- Jupyter
