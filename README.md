# 2048 Game - Python Implementation with Reinforcement Learning

## Overview

This repository contains a Python implementation of the **2048 game**, where players combine matching tiles on a grid to reach the highest possible value, typically aiming to reach the 2048 tile. Additionally, this project aims to **train an AI model** using **reinforcement learning (RL)** to play the game autonomously.

The game supports:
- Customizable grid sizes
- Various movement modes
- Automatic and random gameplay
- In-depth performance tracking
- (WIP) Reinforcement learning to train a model to play optimally

The AI is designed to interact with the game environment, learning how to maximize its score through trial and error, improving its gameplay strategies over time.

## Table of Contents
- [Features](#features)
- [How to Play](#how-to-play)
- [Gameplay Mechanics](#gameplay-mechanics)
- [Game Rules](#game-rules)
- [Statistics & Scoring](#statistics--scoring)
- [Final Score Calculation](#final-score-calculation)
- [Installation](#installation)
- [License](#license)

---

## Features

- **Multiple Grid Sizes**: Customize the grid size (e.g., 3x3, 4x4, 6x6, etc.).
- **Movement Options**: Use **W** (up), **A** (left), **S** (down), **D** (right) for manual movement. Press **R** for random automatic play, or **P** for a predefined sequence of moves.
- **Reinforcement Learning Integration**: An AI model that learns how to play the game optimally through interaction with the environment.
- **Detailed Statistics**: Track the number of moves, highest tile, missed merge opportunities, illegal moves, and more.
- **Game Simulation**: Simulate the game automatically with the **P** (predefined) or **R** (random) modes.

---

## How to Play

1. **Start a New Game**: 
   Upon launching, the game will prompt you to choose a grid size. After selecting, the game will automatically initialize the grid and display the current board state.
   
2. **Making Moves**: 
   Use the following keys to make your moves:
   - **W**: Move tiles up.
   - **A**: Move tiles left.
   - **S**: Move tiles down.
   - **D**: Move tiles right.
   
   After each move, a new tile will be randomly placed on the board, typically either a 2 or a 4.

3. **Special Modes**:
   - **P**: The game will automatically perform moves based on a predefined sequence until the board doesn't change anymore.
   - **R**: Random movements will be made automatically until the game ends.

4. **Goal**: Combine tiles of the same value to form higher-value tiles, and aim to reach the 2048 tile. The game ends when there are no valid moves left.

---

## Gameplay Mechanics

- **Tile Merging**: When two adjacent (or separated by empty space) tiles with the same number are aligned in the direction of the move, they will combine into one tile with double the value.
- **Random Tile Generation**: After every valid move, a new tile (either a **2** or **4**) is placed on a random empty spot on the board.
- **Winning Condition**: The game is won when a tile with the value **2048** is created. The player may continue to play to achieve a higher score.
- **Losing Condition**: The game ends when no more valid moves are available, i.e., when all tiles are filled, and there are no adjacent equal tiles for merging.

---

## Game Rules

1. **Tile Values**: Tiles start at **2** or **4** and merge to form higher values (e.g., **2 → 4 → 8 → 16 → 32 → 64 → 128 → 256 → 512 → 1024 → 2048**).
   
2. **Movement Restrictions**: 
   - **W, A, S, D** moves are allowed to slide tiles in their respective directions. 
   - A move that doesn’t change the board (no tiles merge or move) counts as an **illegal move**.
   
3. **Game End**: The game ends when either:
   - The player wins by creating a tile with the value **2048**.
   - No valid moves are left (i.e., when all tiles are filled, and there are no adjacent equal tiles for merging).

---

## Statistics & Scoring

### In-Game Statistics:
The game tracks the following key metrics throughout the gameplay:

1. **Total Moves**: The number of moves made during the game.
2. **Highest Number Achieved**: The highest tile value reached on the board.
3. **Average Empty Spaces**: The average number of empty spaces across all board states during the game.
4. **Missed Merge Opportunities**: The count of adjacent tiles that could have merged but weren't merged, representing missed optimization opportunities. Small tiles (<16) do not count.
5. **Illegal Moves**: The number of moves where no tiles were reduced.

---

## Final Score Calculation

The **Final Score** is calculated using the following formula:

$$
\text{Final Score} = w_1 \cdot \min\left(1, \frac{m}{M}\right) + w_2 \cdot \min\left(1, \frac{n}{N}\right) + w_3 \cdot \min\left(1, \frac{E}{k^2}\right) + w_4 \cdot \left(1 - \min\left(1, \frac{P}{30}\right)\right) + w_5 \cdot \left(1 - \min\left(1, \frac{I}{20}\right)\right)
$$

Where:
- **k**: The size of the grid (e.g., 4 for a 4x4 grid)
- **w₁**: Weight for **Total Moves** (how many moves were made during the game). This represents how efficiently the player can complete the game with fewer moves. A higher weight for **w₁** encourages longer, more efficient games.
- **w₂**: Weight for **Highest Tile Achieved** (the highest tile value reached during the game). This weight prioritizes achieving a high tile, which is a key indicator of success in the game.
- **w₃**: Weight for **Average Empty Spaces** (how efficiently the player used the grid space). This weight encourages players to use the grid effectively and avoid leaving too many empty spaces, which could indicate inefficient moves.
- **w₄**: Weight for **Missed Merge Opportunities** (the number of times a merge was possible but not performed). This weight penalizes players for missing opportunities to merge tiles, which is critical for progressing in the game.
- **w₅**: Weight for **Illegal Moves** (the number of illegal moves made). This weight penalizes players for making moves that don't reduce numbers, which is a clear indicator of poor gameplay.
- **m**: Total number of moves made during the game  
- **M**: The maximum expected number of moves for the grid size (varies based on the grid size). For example, in a standard 4x4 grid, this might be around 1000 moves, while for a larger grid (e.g., 10x10), it might be higher.
- **n**: The highest tile number achieved during the game  
- **N**: The maximum expected tile value for the grid size. For a standard 4x4 grid, this would be **2048**, but for larger grids, the maximum achievable tile could be higher (e.g., **4096** for a larger grid).
- **E**: Average number of empty spaces across all board states  
- **P**: The number of missed merge opportunities
- **I**: The number of illegal moves made during the game