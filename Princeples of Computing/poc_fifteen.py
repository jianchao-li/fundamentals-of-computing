"""
Loyd's Fifteen puzzle - solver and visualizer
Note that solved configuration has the blank (zero) tile in upper left
Use the arrow keys to swap this tile with its neighbors
"""

import poc_fifteen_gui

class Puzzle:
    """
    Class representation for the Fifteen puzzle
    """

    def __init__(self, puzzle_height, puzzle_width, initial_grid=None):
        """
        Initialize puzzle with default height and width
        Returns a Puzzle object
        """
        self._height = puzzle_height
        self._width = puzzle_width
        self._grid = [[col + puzzle_width * row 
                       for col in range(self._width)] 
                      for row in range(self._height)]
        if initial_grid != None:
            for row in range(puzzle_height):
                for col in range(puzzle_width):
                    self._grid[row][col] = initial_grid[row][col]
            
    def __str__(self):
        """
        Generate string representaion for puzzle
        Returns a string
        """
        ans = ""
        for row in range(self._height):
            ans += str(self._grid[row])
            ans += "\n"
        return ans

    #####################################
    # GUI methods

    def get_height(self):
        """
        Getter for puzzle height
        Returns an integer
        """
        return self._height

    def get_width(self):
        """
        Getter for puzzle width
        Returns an integer
        """
        return self._width

    def get_number(self, row, col):
        """
        Getter for the number at tile position (row, col)
        Returns an integer
        """
        return self._grid[row][col]

    def set_number(self, row, col, value):
        """
        Setter for the number at tile position (row, col)
        """
        self._grid[row][col] = value

    def clone(self):
        """
        Make a copy of the puzzle to update during solving
        Returns a Puzzle object
        """
        new_puzzle = Puzzle(self._height, self._width, self._grid)
        return new_puzzle

    ########################################################
    # Core puzzle methods

    def current_position(self, solved_row, solved_col):
        """
        Locate the current position of the tile that will be at
        position (solved_row, solved_col) when the puzzle is solved
        Returns a tuple of two integers        
        """
        solved_value = (solved_col + self._width * solved_row)

        for row in range(self._height):
            for col in range(self._width):
                if self._grid[row][col] == solved_value:
                    return (row, col)
        assert False, "Value " + str(solved_value) + " not found"

    def update_puzzle(self, move_string):
        """
        Updates the puzzle state based on the provided move string
        """
        zero_row, zero_col = self.current_position(0, 0)
        for direction in move_string:
            if direction == "l":
                assert zero_col > 0, "move off grid: " + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row][zero_col - 1]
                self._grid[zero_row][zero_col - 1] = 0
                zero_col -= 1
            elif direction == "r":
                assert zero_col < self._width - 1, "move off grid: " + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row][zero_col + 1]
                self._grid[zero_row][zero_col + 1] = 0
                zero_col += 1
            elif direction == "u":
                assert zero_row > 0, "move off grid: " + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row - 1][zero_col]
                self._grid[zero_row - 1][zero_col] = 0
                zero_row -= 1
            elif direction == "d":
                assert zero_row < self._height - 1, "move off grid: " + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row + 1][zero_col]
                self._grid[zero_row + 1][zero_col] = 0
                zero_row += 1
            else:
                assert False, "invalid direction: " + direction

    ##################################################################
    # Phase one methods

    def lower_row_invariant(self, target_row, target_col):
        """
        Check whether the puzzle satisfies the specified invariant
        at the given position in the bottom rows of the puzzle (target_row > 1)
        Returns a boolean
        """
        # Tile zero is positioned at (i, j)
        if self.current_position(0, 0) != (target_row, target_col):
            return False
        # All tiles in row i to the right of position (i, j) 
        # are positioned at their solved location
        for col in range(target_col + 1, self.get_width()):
            if self.current_position(target_row, col) != (target_row, col):
                return False
        # All tiles in rows i + 1 or below are positioned 
        # at their solved location
        for row in range(target_row + 1, self.get_height()):
            for col in range(self.get_width()):
                if self.current_position(row, col) != (row, col):
                    return False
        return True
    
    def move_to_current(self, target_pos, current_pos):
        """
        Move from the target position to the current position
        Returns a move string
        """
        move_string = ""
        offset_row = target_pos[0] - current_pos[0]
        offset_col = target_pos[1] - current_pos[1]
        move_string += "u" * offset_row
        if offset_col > 0:
            move_string += "l" * offset_col
        else:
            move_string += "r" * abs(offset_col)
        return move_string
    
    def position_interior_tile(self, current_pos, target_pos):
        """
        Position the tile at current position to target position
        Returns a move string
        """
        move_string = ""
        move_string += self.move_to_current(target_pos, current_pos)
        if current_pos[0] == target_pos[0]:
            if current_pos[1] < target_pos[1]:
                # target tile is to the left of the zero tile at the same row
                offset_col = target_pos[1] - current_pos[1]
                move_string += "urrdl" * (offset_col - 1)
                return move_string
            else:
                # target_tile is to the right of the zero tile at the same row
                offset_col = current_pos[1] - target_pos[1]
                move_string += "ulldr" * (offset_col - 1)
                return move_string
        else:
            # target tile is above the zero tile
            offset_row = target_pos[0] - current_pos[0]
            offset_col = target_pos[1] - current_pos[1]
            if offset_col > 0:
                # target tile is to the left of the zero tile
                move_string += "drrul" * (offset_col - 1)
                move_string += "dru"
            elif offset_col < 0:
                if current_pos[0] == target_pos[0] - 1 and current_pos[0] > 0:
                    # target tile cannot be moved down
                    move_string += "ulldr" * (abs(offset_col) - 1)
                    move_string += "ullddru"
                else:
                    # target tile has to be moved down
                    move_string += "dllur" * (abs(offset_col) - 1)
                    move_string += "dlu"
            if offset_row == 1:
                move_string += "ld"
            else:
                move_string += "lddru" * (offset_row - 1)
            return move_string
    
    def solve_interior_tile(self, target_row, target_col):
        """
        Place correct tile at target position
        Updates puzzle and returns a move string
        """
        # invariant check
        assert self.lower_row_invariant(target_row, target_col)
        
        move_string = ""
        
        # reposition target tile at current position to target position
        current_pos = self.current_position(target_row, target_col)
        move_string += self.position_interior_tile(current_pos, (target_row, target_col))
        self.update_puzzle(move_string)
        if self.lower_row_invariant(target_row, target_col - 1):
            assert self.lower_row_invariant(target_row, target_col - 1)
            return move_string
        else:
            # maintain the invariant
            maintain_string = "ld"
            self.update_puzzle(maintain_string)
            move_string += maintain_string
            
            assert self.lower_row_invariant(target_row, target_col - 1)
            return move_string

    def solve_col0_tile(self, target_row):
        """
        Solve tile in column zero on specified row (> 1)
        Updates puzzle and returns a move string
        """
        # invariant check
        assert self.lower_row_invariant(target_row, 0)
        
        move_string = ""
        
        current_pos = self.current_position(target_row, 0)
        if current_pos == (target_row - 1, 0):
            # the lucky case
            move_string += "u"
            move_string += "r" * (self.get_width() - 1)
            self.update_puzzle(move_string)
            
            assert self.lower_row_invariant(target_row - 1, self.get_width() - 1)
            return move_string
        else:
            # the trickier case
            
            # move zero tile to (i - 1, 0) and target_tile to (i - 1, 1)
            move_string += "ur"
            self.update_puzzle(move_string)
            current_pos = self.current_position(target_row, 0)
            reposition_string = self.position_interior_tile(current_pos, (target_row - 1, 1))
            move_string += reposition_string
            self.update_puzzle(reposition_string)
            zero_pos = self.current_position(0, 0)
            if zero_pos[0] < target_row - 1:
                maintain_string = "ld"
            elif zero_pos[1] > 1:
                maintain_string = "ulld"
            else:
                maintain_string = ""
            move_string += maintain_string
            self.update_puzzle(maintain_string)
            
            # solve a 3 by 2 puzzle
            solve_string = "ruldrdlurdluurddlu"
            solve_string += "r" * (self.get_width() - 1)
            self.update_puzzle(solve_string)
            move_string += solve_string
            
            assert self.lower_row_invariant(target_row - 1, self.get_width() - 1)
            return move_string
        
    #############################################################
    # Phase two methods

    def row0_invariant(self, target_col):
        """
        Check whether the puzzle satisfies the row zero invariant
        at the given column (target_col > 1)
        Returns a boolean
        """
        # zero tile should be at (0, target_col)
        if self.current_position(0, 0) != (0, target_col):
            return False
        # tiles right to the zero tile at row 0 should be solved
        for col in range(target_col + 1, self.get_width()):
            if self.current_position(0, col) != (0, col):
                return False
        # tiles below and right to the zero tile at row 1 should be solved
        for col in range(target_col, self.get_width()):
            if self.current_position(1, col) != (1, col):
                return False
        # all below rows should be solved
        for row in range(2, self.get_height()):
            for col in range(self.get_width()):
                if self.current_position(row, col) != (row, col):
                    return False
        return True

    def row1_invariant(self, target_col):
        """
        Check whether the puzzle satisfies the row one invariant
        at the given column (target_col > 1)
        Returns a boolean
        """
        # zero tile should be at (1, target_col)
        if self.current_position(0, 0) != (1, target_col):
            return False
        # tiles right to the zero tile should be solved at both row 0 and row 1
        for col in range(target_col + 1, self.get_width()):
            if self.current_position(0, col) != (0, col):
                return False
            if self.current_position(1, col) != (1, col):
                return False
        # all below rows should be solved
        for row in range(2, self.get_height()):
            for col in range(self.get_width()):
                if self.current_position(row, col) != (row, col):
                    return False
        return True

    def solve_row0_tile(self, target_col):
        """
        Solve the tile in row zero at the specified column
        Updates puzzle and returns a move string
        """
        # sanity check
        assert self.row0_invariant(target_col)
        
        move_string = ""
        
        current_pos = self.current_position(0, target_col)
        if current_pos == (0, target_col - 1):
            # the lucky case
            move_string += "ld"
            self.update_puzzle(move_string)
            
            assert self.row1_invariant(target_col - 1)
            return move_string
        else:
            # the trickier case
            
            # reposition target tile to (1, j - 1) and zero tile to (1, j - 2)
            move_string += "ld"
            self.update_puzzle(move_string)
            current_pos = self.current_position(0, target_col)
            reposition_string = self.position_interior_tile(current_pos, (1, target_col - 1))
            self.update_puzzle(reposition_string)
            move_string += reposition_string
            
            # solve a 2 by 3 puzzle
            solve_string = "urdlurrdluldrruld"
            self.update_puzzle(solve_string)
            move_string += solve_string
        
            assert self.row1_invariant(target_col - 1)
            return move_string

    def solve_row1_tile(self, target_col):
        """
        Solve the tile in row one at the specified column
        Updates puzzle and returns a move string
        """
        # sanity check
        assert self.row1_invariant(target_col)
        
        move_string = ""
        
        # move to the current position
        current_pos = self.current_position(1, target_col)
        move_string += self.position_interior_tile(current_pos, (1, target_col))
        self.update_puzzle(move_string)
        
        # maintain the invariant
        zero_pos = self.current_position(0, 0)
        zero_offset_row = zero_pos[0]
        zero_offset_col = target_col - zero_pos[1]
        maintain_string = "u" * zero_offset_row + "r" * zero_offset_col
        self.update_puzzle(maintain_string)
        move_string += maintain_string
        
        assert self.row0_invariant(target_col)
        return move_string

    ###########################################################
    # Phase 3 methods

    def solve_2x2(self):
        """
        Solve the upper left 2x2 part of the puzzle
        Updates the puzzle and returns a move string
        """
        # sanity check
        assert self.row1_invariant(1)
        
        current_pos = self.current_position(0, 1)
        if current_pos == (0, 0):
            move_string = "ul"
        elif current_pos == (0, 1):
            move_string = "lu"
        elif current_pos == (1, 0):
            move_string = "uldrul"
        self.update_puzzle(move_string)
        
        assert self.row0_invariant(0)
        return move_string
    
    def solve_puzzle(self):
        """
        Generate a solution string for a puzzle
        Updates the puzzle and returns a move string
        """
        move_string = ""
        zero_pos = self.current_position(0, 0)
        if not self.row0_invariant(0) and zero_pos != (self.get_height() - 1, self.get_height() - 1):
            zero_offset_row = self.get_height() - 1 - zero_pos[0]
            zero_offset_col = self.get_width() - 1 - zero_pos[1]
            init_string = "r" * zero_offset_col + "d" * zero_offset_row
            self.update_puzzle(init_string)
            move_string += init_string
        while not self.row0_invariant(0):
            zero_pos = self.current_position(0, 0)
            if zero_pos[0] > 1 and zero_pos[1] > 0:
                move_string += self.solve_interior_tile(zero_pos[0], zero_pos[1])
            elif zero_pos[0] > 1 and zero_pos[1] == 0:
                move_string += self.solve_col0_tile(zero_pos[0])
            elif zero_pos[0] == 1 and zero_pos[1] > 1:
                move_string += self.solve_row1_tile(zero_pos[1])
            elif zero_pos[0] == 0 and zero_pos[1] > 1:
                move_string += self.solve_row0_tile(zero_pos[1])
            else:
                move_string += self.solve_2x2()
        return move_string

# Start interactive simulation
# configuration = [[15, 16, 0, 3, 4], [5, 6, 7, 8, 9], [10, 11, 12, 13, 14], [1, 2, 17, 18, 19]]
# poc_fifteen_gui.FifteenGUI(Puzzle(4, 5, configuration))