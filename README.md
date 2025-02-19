# Poker Hand Simulator with Monte Carlo Odds

This repository contains a Texas Hold'em hand simulator that uses a Monte Carlo simulation to estimate winning odds. The project is split into two modules:

- **`main.py`**: Deals random hero and community cards and displays the game progression (Pre-flop, Flop, Turn, River).
- **`montecarlo.py`**: Contains functions for hand evaluation and the Monte Carlo simulation to calculate win percentages.

## Features

- **Random Hand Generation**: Each execution deals a random hero hand and community cards.
- **Proper Card Symbols**: Cards are represented with standard suit symbols (♥, ♦, ♣, ♠).
- **Monte Carlo Simulation**: Estimates win odds at each stage of the game by simulating thousands of random outcomes.
- **Stage-by-Stage Output**: Displays the hand progression and corresponding win percentage estimates.

## Requirements

- Python 3.x

## Usage

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/yourusername/your-repo-name.git
   cd your-repo-name