# 🎰 Slot Machine Game - Python + Tkinter + MySQL

A fun and interactive **Slot Machine Game** built using **Python's Tkinter GUI** framework and integrated with a **MySQL database** for storing player data and bet results.

## Features

- 🎮 Simple 3x3 Slot Grid Interface
- 💰 Adjustable Betting System with Min/Max Limits
- 🧠 Randomized Symbol Logic with Weighted Probabilities
- 🧾 MySQL Integration for:
  - Storing User Bets
  - Game Results Logging
  - Player Balance Tracking
- ❌ Graceful Error Handling for Invalid Inputs & Database Failures
- 🧱 Modular and Maintainable Code Structure

##  Tech Stack

- **Language:** Python 3.x  
- **GUI:** Tkinter  
- **Database:** MySQL (via `mysql-connector-python`)  
- **IDE Recommended:** VS Code / PyCharm  

##  Game Logic

- Player starts with a balance.
- Select the number of lines (1 to 3) to bet on and the bet per line.
- Symbols (`A`, `B`, `C`, `D`) are randomly drawn with specific frequencies and payout values.
- If a full line has matching symbols, the player wins based on the symbol's value.
- Balance is updated after each spin and stored in the database.

##  Database Schema

```sql
CREATE DATABASE IF NOT EXISTS slot_machine;

USE slot_machine;

CREATE TABLE IF NOT EXISTS players (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255),
    balance INT DEFAULT 1000
);

CREATE TABLE IF NOT EXISTS game_results (
    id INT AUTO_INCREMENT PRIMARY KEY,
    player_id INT,
    bet INT,
    lines INT,
    result VARCHAR(255),
    winnings INT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (player_id) REFERENCES players(id)
);
