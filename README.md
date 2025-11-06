# Sudoku CSP Solver

A Constraint Satisfaction Problem (CSP) solver for Sudoku puzzles implemented in Python. This project demonstrates an AI implementation of a heuristic-informed backtracking search through a CSP state space

## Overview

This Sudoku solver implements a backtracking CSP algorithm with configurable heuristics to efficiently solve Sudoku puzzles. The solver uses constraint propagation through forward checking and supports multiple search optimization techniques.

### Key CSP Concepts Implemented:
- **Variables**: Each cell in the 9×9 Sudoku grid
- **Domain**: Possible values (1-9) for each cell
- **Constraints**: Row, column, and 3×3 subgrid uniqueness constraints
- **Search Algorithm**: Backtracking with constraint propagation
- **Heuristics**: MRV, Degree, and LCV for search optimization

## Features

### Search Heuristics
- ✅ **MRV (Minimum Remaining Values)**: Select variables with smallest domains
- ✅ **Degree Heuristic**: Break ties by choosing most constrained variables
- ✅ **LCV (Least Constraining Value)**: Order values to preserve flexibility

## Installation

### Prerequisites
- Python 3.6 or higher
- Standard Python libraries (no external dependencies)

### Setup
```bash
# Clone the repository
git clone <repository-url>
cd sudoku-csp

# Verify Python installation
python3 --version

# Test the solver
python3 sudoku-solver.py puzzles.txt
```

## Usage

### Basic Usage
```bash
# Solve puzzles with optimal settings (default)
python3 sudoku-solver.py puzzles.txt

# Show help and available options
python3 sudoku-solver.py --help
```

### Advanced Options
```bash
# Disable specific heuristics for comparison
python3 sudoku-solver.py --no-mrv puzzles.txt          # Disable MRV heuristic
python3 sudoku-solver.py --no-degree puzzles.txt       # Disable degree heuristic
python3 sudoku-solver.py --no-mrv --no-degree puzzles.txt  # Disable both heuristics

# Limit number of puzzles to solve
python3 sudoku-solver.py --max-solve 5 puzzles.txt
```

### Input Format
Puzzles should be in a text file with one puzzle per line, using:
- **Digits 1-9**: Given clues
- **Periods (.)**: Empty cells

Example puzzle line:
```
.18...7.....3..2...7...........71...6......4.3........4..5....3.2..8...........6.
```

### Output Format
The solver displays:
1. **Configuration**: Which heuristics are enabled
2. **Initial puzzle**: Visual representation of the input
3. **Solution**: Completed puzzle (if solvable)
4. **Statistics**: Timing and performance metrics

## Implementation Details

### Core Classes

#### `Cell` Class
Represents individual Sudoku cells with:
- **Domain management**: Track possible values
- **Assignment operations**: Set and unset values  
- **Constraint checking**: Domain reduction operations

```python
cell = Cell()                    # Initialize with domain [1,2,3,4,5,6,7,8,9]
cell.assign_value(5)            # Set value to 5, domain becomes [5]
cell.remove_value(3)            # Remove 3 from domain
```

#### `Sudoku` Class
Manages the complete puzzle state with:
- **Constructor overloading**: Multiple initialization methods
- **Constraint propagation**: Forward checking implementation
- **Neighbor management**: Efficient constraint graph representation

```python
# Three ways to create puzzles
puzzle1 = Sudoku()                          # Blank puzzle
puzzle2 = Sudoku(puzzle_string)             # From string
puzzle3 = Sudoku(existing_puzzle)           # Copy constructor
```

### Search Algorithm

The backtracking algorithm follows this structure:
1. **Base case**: Check if puzzle is solved
2. **Variable selection**: Choose next cell using heuristics
3. **Value ordering**: Try values in optimal order
4. **Constraint checking**: Use forward checking
5. **Recursive search**: Explore valid assignments
6. **Backtrack**: Undo assignments on failure

## Heuristics

### Variable Selection Heuristics

#### MRV (Minimum Remaining Values)
- **Purpose**: Select variables with smallest domains first
- **Benefit**: Reduces branching factor by tackling constrained variables early
- **Impact**: ~18.9x speedup over no heuristics

#### Degree Heuristic  
- **Purpose**: Break MRV ties by selecting most constraining variables
- **Benefit**: Provides additional constraint propagation
- **Impact**: Additional 1.4x speedup when combined with MRV

### Value Ordering Heuristic

#### LCV (Least Constraining Value)
- **Purpose**: Order values to preserve maximum flexibility
- **Implementation**: Sort by number of constraints imposed on neighbors
- **Complexity**: O(k log k) where k ≤ 9, effectively constant time

## Performance Analysis

Based on comprehensive testing with 7 diverse puzzles:

| Configuration | Avg Time/Puzzle | Speedup Factor | Success Rate |
|---------------|-----------------|----------------|--------------|
| **Both Heuristics** 🏆 | 0.34 seconds | 26.3x | 100% |
| **MRV Only** | 0.48 seconds | 18.9x | 100% |
| **No Heuristics** | 9.06 seconds | 1.0x (baseline) | 100% |
| **Degree Only** | Timeout | N/A | 0% |

### Key Insights
- **Combined heuristics**: Provide optimal performance (default setting)
- **MRV dominance**: Most significant performance impact
- **Degree contribution**: Meaningful but secondary improvement  
- **Degree alone**: Completely ineffective without MRV

### Areas for Enhancement
- **Additional heuristics**: Most constrained variable, value symmetry
- **Optimization**: Further algorithmic improvements  
- **Input formats**: Support for different puzzle representations
- **Visualization**: Graphical puzzle display and solving animation
- **Parallelization**: Multi-threaded solving for puzzle batches

## Algorithm Complexity

- **Time Complexity**: O(9^n) worst case, where n is empty cells
- **Space Complexity**: O(n) for recursion depth
- **Practical Performance**: Sub-second solving for most puzzles with heuristics
- **Heuristic Impact**: Reduces effective branching factor significantly

## Educational Value

This implementation demonstrates:
- **CSP fundamentals**: Variables, domains, constraints
- **Search algorithms**: Backtracking with pruning
- **Heuristic design**: Principled search optimization  
- **Performance analysis**: Empirical algorithm evaluation
- **Software engineering**: Modular design, testing, documentation

## License

This project is part of an academic assignment for CS 470 (Artificial Intelligence). Please respect academic integrity policies when using this code.

---

**Authors**: Chris Archibald, Trent Welling  
**Course**: CS 470 - Artificial Intelligence  
**Institution**: Brigham Young University

## AI Disclosure
README partially generated with Claude Sonnet 4