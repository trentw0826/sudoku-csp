from __future__ import print_function
import sys
import time
import argparse

# Code for AI Sudoku Programming Assignment
# Written by Chris Archibald, modified and extended by Trent Welling
# archibald@cs.byu.edu, tdw57@byu.edu

MAX_DOMAIN_LEN = 9


class Cell:
    """
    This class represents a variable corresponding to an
    individual cell in the Sudoku puzzle
    It's domain is the set of digits it could be (1-9)

    """

    def __init__(self):

        # The domain contains a list of the values that this variable could take on
        self.domain = list(range(1, 10))

        # The value assigned to this variable if it has been assigned
        # None means that it hasn't been assigned
        self.value = None

    def __str__(self):
        """
        Return a string representation of this cell
        """
        return str(self.value) if self.value else "."

    def __repr__(self):
        """
        Return a string representation of this cell for storage purposes
        Displays both the assigned value (or '.' if unassigned) and the current domain.
        """
        return str((self.__str__(), self.domain))

    def assign_value(self, value):
        """
        Assign [value] to be this variable's value
        This function sets the domain to be only this value, and sets the value to be the value
        """
        self.domain = [value]
        self.value = value

    def set_domain(self, domain):
        """
        Set the domain of this variable to be [domain]
        Set the value to unassigned (= None)
        """
        self.domain = domain[:]
        self.value = None

    def domain_len(self):
        """
        Return the length of this variable's domain
        """
        return len(self.domain)

    def remove_value(self, value):
        """
        Remove [value] from this variable's domain
        Return False if the domain for this variable is now empty
        Return True if there is still at least one variable in the domain
        """
        if value in self.domain:
            self.domain.remove(value)
        if len(self.domain) == 0:
            return False
        return True

    def copy_cell(self, other):
        """
        Set the domain and value of this cell to that of the input other cell
        """
        self.domain = other.domain[:]
        self.value = other.value

    def is_unassigned(self):
        """
        Return True if this cell has not been assigned a value (value is None)
        Return False if this cell has been assigned a value
        """
        return self.value is None


class Sudoku:
    """
    This class contains all of the cells for an entire Sudoku puzzle
    """

    def __init__(self, source=None):
        """
        Initialize this puzzle with constructor overloading:
        - Sudoku(): Create blank puzzle (all cells initially empty)
        - Sudoku(other_puzzle): Create copy of another Sudoku puzzle
        - Sudoku(puzzle_string): Create puzzle from string representation
        
        Args:
            source: None for blank puzzle, Sudoku object for copy, or string for initialization
        """
        # Always start by creating the grid structure
        self.cells = [[Cell() for j in range(9)] for i in range(9)]
        
        if source is None:
            # Case 1: Blank puzzle (default behavior)
            pass
        elif isinstance(source, Sudoku):
            # Case 2: Copy constructor
            self.copy_puzzle(source)
        elif isinstance(source, str):
            # Case 3: Initialize from string representation
            self.input_puzzle(source)
        else:
            raise TypeError(f"Sudoku constructor expects None, Sudoku object, or string, got {type(source)}")

    def __repr__(self):
        """
        Return a single string representation of the puzzle. For storage purposes
        """
        return "".join(str(self.cell_at(r, c)) for r in range(9) for c in range(9))

    def __str__(self):
        """
        Return a human-readable string representation of the puzzle
        """
        out = []
        for r in range(9):
            if (r % 3) == 0 and r > 0:
                out.append("\n")
            for c in range(9):
                if (c % 3) == 0 and c > 0:
                    out.append(" ")
                out.append(
                    str(self.cell_at(r, c).value)
                    if self.cell_at(r, c).value is not None
                    else "."
                )
            out.append("\n")
        return "".join(out)

    def copy_puzzle(self, other):
        """
        Set all of this puzzle's cells to be the same as the other puzzle (input to function)
        """
        [
            [self.cell_at(j, i).copy_cell(other.cell_at(j, i)) for j in range(9)]
            for i in range(9)
        ]

    def is_solved(self):
        """
        Return true if every cell has been assigned a value
        This assumes that only valid assignments have been made
        """
        for r in range(9):
            for c in range(9):
                if self.cell_at(r, c).is_unassigned():
                    return False
        return True

    def input_puzzle(self, puzzle_string):
        """
        Initialize this puzzle to match the starting state specified by [puzzle string]
        This is done by assigning all of the cells to be their given value (if specified)
        Then forward-checking is performed for every variable assignment that has been made
        """

        # Cycle through the puzzle and assign all the cells that are given in the input string
        r = 0
        c = 0
        for v in puzzle_string:
            if v != ".":
                self.cell_at(r, c).assign_value(int(v))
            c += 1
            if c > 8:
                c = 0
                r += 1

        # Cycle through the puzzle and perform forward checking for every variable that
        # was assigned a value
        for r in range(9):
            for c in range(9):
                if not self.cell_at(r, c).is_unassigned():
                    success = self.forward_check(r, c, self.cell_at(r, c).value)
                    if not success:
                        ### This puzzle has some serious problem.  Exit now.
                        print("Contradiction in Puzzle! Invalid input. Exiting")
                        print(" Puzzle string: ", puzzle_string)
                        sys.exit()

    def get_neighbors(self, row, column):
        """
        Return a set of (row, column) tuples corresponding to the neighbors
        of the cell at [row], [column]
        Neighbors are those cells in the same row, column, or grid
        """
        neighbors = set()

        # Add row and column neighbors
        for i in range(9):
            if i != column:
                neighbors.add(self.cell_at(row, i))
            if i != row:
                neighbors.add(self.cell_at(i, column))

        # Add grid neighbors
        grid, cell = self.get_grid_cell(row, column)
        base_r = 3 * int(grid / 3)
        base_c = 3 * (grid % 3)
        for off_r in range(3):
            for off_c in range(3):
                r = base_r + off_r
                c = base_c + off_c
                if r != row or c != column:
                    neighbors.add(self.cell_at(r, c))

        return neighbors

    def forward_check(self, row, column, value, mode="remove"):
        """
        Perform forward checking for the assignment of [value] to the cell at [row], [column]
        Return False if any domain is empty as a result of forward checking, True otherwise.
        If [mode] == count, then values shouldn't be removed, but merely a count returned
        of how many values forward checking would remove
        """

        neighbors = self.get_neighbors(row, column)
        if mode == "remove":
            for neighbor in neighbors:
                # Skip assigned neighbors
                if not neighbor.is_unassigned():
                    continue
                if not neighbor.remove_value(value):
                    return False  # Empty domain created
            return True
        elif mode == "count":
            count = 0
            for neighbor in neighbors:
                # Skip assigned neighbors
                if not neighbor.is_unassigned():
                    continue
                if value in neighbor.domain:
                    count += 1
            return count

    def get_row_column(self, grid, cell):
        """
        Return the row and column indices for a given [grid] and [cell] location
        """
        base_r = 3 * int(grid / 3)
        base_c = 3 * (grid % 3)
        off_r = int(cell / 3)
        off_c = cell % 3
        return base_r + off_r, base_c + off_c

    def get_grid_cell(self, row, column):
        """
        Return the grid and cell indices for a given [row] and [column] location
        """
        grid = 3 * int(row / 3) + int(column / 3)
        base_r = 3 * int(grid / 3)
        base_c = 3 * (grid % 3)
        off_r = row - base_r
        off_c = column - base_c
        cell = 3 * int(off_r) + int(off_c)
        return grid, cell

    def cell_at(self, row, col):
        """
        Return the Cell object at the given row and column position
        This is a helper function to access cells more cleanly
        """
        return self.cells[row][col]


# Other functions (not in Sudoku class)
# When [puzzle] is an input
# it is an object of the Sudoku puzzle class [Sudoku]


def mrv(puzzle, unassigned):
    """
    Return a list of the (row, column) tuples, out of the list of [unassigned] cells given
    that have the minimum remaining values
    [unassigned] is a list of (row, column) tuples corresponding to cell locations
    """

    min_len = MAX_DOMAIN_LEN + 1
    mrv_variables = []
    for u in unassigned:
        d_len = puzzle.cell_at(u[0], u[1]).domain_len()
        if d_len == min_len:
            mrv_variables.append(u)
        if d_len < min_len:
            min_len = d_len
            mrv_variables = [u]

    return mrv_variables


def max_degree(puzzle, tied):
    """
    Return a list of the (row, column) tuples, out of the list of [tied] cells (according to mrv) given
    that have the maximum degree, i.e. are connected to the most unassigned other variables
    This uses the count_constraints function
    """
    max_c = 0
    mc_variables = []
    for t in tied:
        cur_c = count_constraints(puzzle, t[0], t[1])
        if cur_c == max_c:
            mc_variables.append(t)
        if cur_c > max_c:
            max_c = cur_c
            mc_variables = [t]

    return mc_variables


def count_constraints(puzzle, row, column):
    """
    Count the number of unassigned variables that are in the same row, column and grid as
    the input location [row], [column]
    return this number
    This is called by the max_degree function
    """

    neighbors = puzzle.get_neighbors(row, column)
    return sum(neighbor.is_unassigned() for neighbor in neighbors)


def get_unassigned_variables(puzzle):
    """
    Return a list of the variables in the puzzle that haven't been assigned a value
    yet. These will be (row, column) tuples
    """
    unassigned = []
    for r in range(9):
        for c in range(9):
            if puzzle.cell_at(r, c).is_unassigned():
                unassigned.append((r, c))
    return unassigned


def select_variable(puzzle, use_mrv=True, use_degree=True):
    """
    This function will return the row and column location of the variable that should be
    selected next from [puzzle].
    Uses the Minimum Remaining Values heuristic (if use_mrv=True) with
    ties broken by the Degree heuristic (if use_degree=True)
    (additional ties broken arbitrarily)
    """

    # 0. Get the initial list of all unassigned variables
    unassigned = get_unassigned_variables(puzzle)
    
    if not unassigned:
        return None, None

    # 1. Use MRV heuristic if enabled, otherwise use all unassigned variables
    if use_mrv:
        minimum_remaining_values = mrv(puzzle, unassigned)
    else:
        minimum_remaining_values = unassigned

    # If only one variable or MRV disabled, and degree heuristic not needed
    if len(minimum_remaining_values) == 1 or not use_degree:
        return minimum_remaining_values[0][0], minimum_remaining_values[0][1]

    # 2. Refine list to those with maximum degree if enabled
    if use_degree:
        most_constraining_variables = max_degree(puzzle, minimum_remaining_values)
    else:
        most_constraining_variables = minimum_remaining_values

    # 3. Return first variable in the list.  This will be the only one if there was a
    #    unique most constraining variable, or the "alphabetically first" or "arbitrary" one of
    #    them if there were ties
    return most_constraining_variables[0][0], most_constraining_variables[0][1]


def order_values(puzzle, row, column):
    """
    For the variable at the given row and column, return the values of this variables domain,
    ordered by the least-constraining value (LCV) heuristic.
    """

    domain = puzzle.cell_at(row, column).domain[:]
    domain.sort(
        key=lambda value: puzzle.forward_check(row, column, value, mode="count")
    )
    return domain


def backtracking_search(puzzle, use_mrv=True, use_degree=True):
    """
    Perform a recursive backtracking search on [puzzle],
    ensuring that a copy is made of the puzzle
    before modifying it and recursing.

    If unsuccessful, a None value is returned
    If successful, this function returns the solved puzzle object
    """

    # 1. Base case: is [puzzle] solved?
    if puzzle.is_solved():
        return puzzle

    # 2. Select a variable to assign next using specified heuristics
    r, c = select_variable(puzzle, use_mrv, use_degree)
    
    if r is None or c is None:
        return None

    # 3. Select an ordering over the values in the variable's domain
    value_ordering = order_values(puzzle, r, c)

    # 4. For each value in the ordered list:
    for value in value_ordering:

        # 4.1 Create new puzzle and set it to be equal to current puzzle
        new_puzzle = Sudoku(puzzle)

        # 4.2 Assign current value to selected variable (use assign_value())
        new_puzzle.cell_at(r, c).assign_value(value)

        # 4.3 Forward check from this assignment
        success = new_puzzle.forward_check(r, c, value)

        # 4.4 If forward checking detects a problem, then continue to the next value
        if not success:
            continue

        # 4.5 If forward checking doesn't detect problem, then recurse
        solved_puzzle = backtracking_search(new_puzzle, use_mrv, use_degree)

        # 4.6 If the search succeeds then return solved puzzle
        if solved_puzzle:
            return solved_puzzle

        # 4.7 If search is a failure, continue with next value for this variable

    # 5. If all values for the chosen variable failed, return failure (None)
    return None


if __name__ == "__main__":
    
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Sudoku CSP Solver with configurable heuristics')
    parser.add_argument('puzzle_file', help='Path to the puzzle file')
    parser.add_argument('--no-mrv', action='store_true', 
                       help='Disable Minimum Remaining Values heuristic for variable selection')
    parser.add_argument('--no-degree', action='store_true',
                       help='Disable degree heuristic for tie-breaking in variable selection')
    parser.add_argument('--max-solve', type=int, default=10,
                       help='Maximum number of puzzles to solve from the file (default: 10)')
    
    args = parser.parse_args()
    
    # Parse arguments
    use_mrv = not args.no_mrv
    use_degree = not args.no_degree
    max_to_solve = args.max_solve
    
    # Display which heuristics are enabled
    heuristics_used = []
    if use_mrv:
        heuristics_used.append("MRV")
    if use_degree:
        heuristics_used.append("Degree")
    
    if heuristics_used:
        print(f"Using heuristics: {', '.join(heuristics_used)}")
    else:
        print("Using no heuristics (basic variable selection)")

    print("Searching for solutions to puzzles from file: ", args.puzzle_file)

    # Open puzzle file
    try:
        pf = open(args.puzzle_file, "r")
    except FileNotFoundError:
        print(f"Error: File '{args.puzzle_file}' not found.")
        sys.exit(1)

    # Variable to keep track of the number of puzzles solved
    num_solved = 0

    # Start time for solving
    start_time = time.perf_counter()

    # Each puzzle takes up a single line in the file
    for ps in pf.readlines():
        print("\nSearching to find solution to following puzzle:", ps)

        # Create a new puzzle to solve
        p = Sudoku(ps.rstrip())

        # Display the puzzle (before it has been solved)
        print(p)

        # Solve the puzzle with specified heuristics
        success_p = backtracking_search(p, use_mrv=use_mrv, use_degree=use_degree)

        # If the puzzle was solved (success_p is the puzzle, None if no solution)
        if success_p:
            print("\nSuccessfully solved puzzle!  Here is solution:\n")

            # Display the solution to the puzzle
            print(success_p)
            num_solved += 1
            # Update the statistics

        else:
            print("\n!! Unable to solve puzzle !!\n")
            break

        # Stop when we solve enough
        if num_solved > max_to_solve:
            break

    # Record end time
    end_time = time.perf_counter()

    # Close the puzzle file
    pf.close()

    # Print Statistics
    print("\n\n**************")
    print(f"Solved {num_solved} puzzles in {round(end_time - start_time, 4)} seconds.")
    # Compute and display average solve time
    average_time = 0
    if num_solved > 0:
        average_time = (end_time - start_time) / float(num_solved)
    print(f"Average solve time = {round(average_time, 4)} seconds")
