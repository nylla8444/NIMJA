# NIMJA: Nim Game with AI Strategy Helper

NIMJA (Nim Game AI) is a sophisticated implementation of the classic Nim game featuring intelligent AI opponents and a comprehensive strategy helper. The game implements multiple AI algorithms including Nim-sum calculations, minimax with alpha-beta pruning, and advanced endgame strategies.

## 🎮 Features

### Game Modes
- **Player vs Player (PvP)**: Two human players take turns
- **Player vs AI (PvAI)**: Challenge the AI opponent

### Game Variants
- **Normal Nim**: The player who takes the last object **WINS**
- **Misère Nim**: The player who takes the last object **LOSES**

### AI Algorithms
- **Nim-sum Calculation**: Uses XOR operations based on Sprague-Grundy theorem
- **Minimax with Alpha-Beta Pruning**: Optimal move search with pruning optimization
- **Position Evaluation**: Strategic scoring of game states
- **Pattern Matching**: Recognition of winning/forcing positions
- **Endgame Strategy**: Specialized tactics for Misère Nim endgames

### Strategy Helper
- **Real-time Analysis**: Get optimal move suggestions
- **Move Prediction**: See potential move sequences and counter-moves
- **Turn Management**: Practice with both first and second move orders
- **Position Evaluation**: Understand the mathematical principles behind optimal play

## 📋 Prerequisites

- **Python 3.7 or higher**
- **Tkinter** (usually included with Python installations)

### Checking Prerequisites

```powershell
# Check Python version
python --version

# Check if Tkinter is available
python -c "import tkinter; print('Tkinter is available')"
```

## 🚀 Installation

### Option 1: Download and Run
1. Download or clone the repository
2. Navigate to the project directory
3. Run the game directly

### Option 2: Git Clone
```powershell
git clone https://github.com/nylla8444/NIMJA.git
cd "NIMJA"
```

## 🎯 Usage

### Starting the Game
```powershell
python main.py
```

### Game Interface Navigation

#### 1. Mode Selection
- Choose between **Player vs Player** or **Player vs AI**
- Access the **Strategy Helper** for analysis and practice

#### 2. Game Type Selection
- **Normal Nim**: Last player to move wins
- **Misère Nim**: Last player to move loses

#### 3. Playing the Game
- **Game Board**: Visual representation using 'O' characters
- **Input Fields**: 
  - Row (1-4): Select which row to take from
  - Amount: Number of objects to remove
- **Submit Move**: Apply your move to the game

#### 4. Strategy Helper Features
- **Game Mode Toggle**: Switch between Normal and Misère Nim
- **Move Order**: Practice playing first or second
- **Position Analysis**: Get real-time optimal move suggestions
- **Move Predictions**: See AI's top moves and counter-strategies
- **Turn Management**: Input moves and see analysis

## 📁 Project Structure

```
NIMJA/
├── main.py              # Entry point - initializes the game
├── nim_game.py          # Main game logic and GUI management
├── nim_ai.py            # AI algorithms and strategy implementation
├── nim_helper.py        # Strategy helper window and analysis tools
├── .gitignore          # Git ignore patterns
└── README.md           # This documentation file
```

### File Dependencies
```
main.py
└── nim_game.py
    ├── nim_ai.py
    └── nim_helper.py
        └── nim_ai.py
```

## 🧠 AI Strategy Explanation

### Normal Nim Strategy
The AI uses the mathematical concept of **Nim-sum** (XOR of all pile sizes):
- **Winning Position**: Nim-sum ≠ 0 (can force opponent into losing position)
- **Losing Position**: Nim-sum = 0 (opponent has winning strategy)

### Misère Nim Strategy
The AI switches strategy based on game state:
- **Early/Mid Game**: Play like Normal Nim
- **Endgame**: Special rules when few objects remain
  - With all single piles: Leave odd number for opponent
  - With one pile > 1: Reduce to create favorable single pile count

### Algorithm Complexity
- **Nim-sum Calculation**: O(n) where n = number of rows
- **Move Generation**: O(n×m) where m = max objects in a row
- **Position Evaluation**: O(1) constant time
- **Pattern Matching**: O(n log n) due to sorting

## 🎮 How to Play Nim

### Basic Rules
1. Game starts with 4 rows containing 1, 3, 5, and 7 objects respectively
2. Players alternate turns
3. On each turn, remove any number of objects from a single row
4. The goal depends on the game variant:
   - **Normal**: Take the last object to win
   - **Misère**: Force your opponent to take the last object

### Winning Strategy Tips

#### Normal Nim
- Try to leave positions where Nim-sum = 0
- Calculate: Row1 XOR Row2 XOR Row3 XOR Row4
- If result ≠ 0, you can win with optimal play

#### Misère Nim
- Play like Normal Nim until endgame
- In endgame, count piles with >1 object
- Leave odd number of single-object piles for opponent

## 🔧 Troubleshooting

### Common Issues

#### "ModuleNotFoundError: No module named 'tkinter'"
```powershell
# On Ubuntu/Debian
sudo apt-get install python3-tk

# On CentOS/RHEL
sudo yum install tkinter
# or
sudo dnf install python3-tkinter

# On macOS with Homebrew
brew install python-tk
```

#### Game Window Not Appearing
- Ensure you're running Python 3.7+
- Check if display is properly configured (for SSH/remote connections)
- Try running: `python -m tkinter` to test Tkinter installation

#### Performance Issues
- The AI calculations are optimized and should run smoothly
- If experiencing lag, ensure Python is updated to the latest version

### Supported Platforms
- ✅ Windows 10/11
- ✅ macOS 10.14+
- ✅ Linux (Ubuntu 18.04+, Debian 10+, CentOS 7+)

## 🎓 Educational Value

This project demonstrates several computer science concepts:

### Algorithms & Data Structures
- **Game Trees**: Minimax algorithm implementation
- **Optimization**: Alpha-beta pruning for efficient search
- **Bitwise Operations**: XOR for Nim-sum calculations
- **Pattern Recognition**: Strategic position matching

### Mathematical Concepts
- **Combinatorial Game Theory**: Nim-sum and winning/losing positions
- **Sprague-Grundy Theorem**: Foundation of optimal Nim play
- **Game State Evaluation**: Heuristic functions for position assessment

### Software Engineering
- **Modular Design**: Separation of concerns across multiple files
- **Object-Oriented Programming**: Classes for game components
- **GUI Development**: Tkinter interface design
- **Error Handling**: Input validation and exception management

## 🤝 Contributing

This is an educational project. If you'd like to extend it:

### Potential Enhancements
- **Difficulty Levels**: Adjustable AI strength
- **Game Variants**: Different starting configurations
- **Statistics Tracking**: Win/loss records
- **Network Play**: Online multiplayer functionality
- **Sound Effects**: Audio feedback for moves
- **Animation**: Smooth visual transitions

### Code Style
- Follow PEP 8 Python style guidelines
- Add docstrings for new functions
- Include algorithm complexity analysis
- Maintain modular structure

## 📜 License

This project is created for educational purposes. Feel free to use, modify, and distribute for learning and non-commercial purposes.

## 🏆 Acknowledgments

- **Charles Bouton**: Original mathematical analysis of Nim (1901)
- **Sprague-Grundy Theorem**: Foundation for combinatorial game theory
- **Nim Game Theory**: Mathematical optimization in game strategy

---

**Project**: NIMJA  
**Purpose**: Educational demonstration of AI algorithms in game theory  
**Language**: Python 3.7+  
**GUI Framework**: Tkinter  

Enjoy playing and learning with NIMJA! 🎮🧠
