# Connect4

A simple implementation of the classic Connect4 game using Python and Pygame.

## Table of Contents

- [Description](#description)
- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [How to Play](#how-to-play)
- [Customization](#customization)

## Description

This project is a Python implementation of the Connect4 game, where players take turns dropping colored discs into a vertically suspended grid. The goal is to connect four of one's own discs of the same color consecutively vertically, horizontally, or diagonally.

## Features

- Player vs. AI gameplay
- Adjustable difficulty levels (Easy, Medium, Hard)
- Graphical user interface using Pygame
- Minimax algorithm for AI decision-making

## Requirements

- Python 3.x
- Pygame library

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/Halfis/Connect4.git
    ```

2. Install Pygame:

    ```bash
    pip install pygame
    ```

## How to Play

1. Run the game:

    ```bash
    python connect4.py
    ```

2. Select the difficulty level (Easy, Medium, Hard).
3. Click on the column where you want to drop your disc.
4. Try to connect four discs in a row to win!

## Customization

You can customize the game by modifying the constants in the `connect4.py` file, such as grid size, window length for winning, square size, and more.
