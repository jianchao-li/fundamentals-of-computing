"""
Clone of 2048 game.
"""

# import poc_2048_gui
import random

# Directions, DO NOT MODIFY
UP = 1
DOWN = 2
LEFT = 3
RIGHT = 4

# Offsets for computing tile indices in each direction.
# DO NOT MODIFY this dictionary.
OFFSETS = {UP: (1, 0),
           DOWN: (-1, 0),
           LEFT: (0, 1),
           RIGHT: (0, -1)}

def find_next_zero(line, pos):
    """
    Function that finds the next zero entry in line
    starting from pos
    If no zero entry is found, None is returned
    """
    while(pos < len(line)):
        if(line[pos] == 0):
            return pos
        else:
            pos += 1
    return None

def find_next_non_zero(line, pos):
    """
    Function that finds the next non-zero entry in line
    starting from pos
    If no non-zero entry is found, None is returned
    """
    while(pos < len(line)):
        if(line[pos] != 0):
            return pos
        else:
            pos += 1
    return None

def merge(line):
    """
    Helper function that merges a single row or column in 2048
    """
    
    # copy the line to a merged line
    merged_line = list(line)
    
    # reference position
    ref_pos = 0
    
    # index of next non-zero entry
    next_non_zero_ind = find_next_non_zero(line, ref_pos + 1)
    
    # merge the line
    while(next_non_zero_ind != None):
        if(merged_line[ref_pos] == 0):
            merged_line[ref_pos] = merged_line[next_non_zero_ind]
            merged_line[next_non_zero_ind] = 0
        elif(merged_line[ref_pos] == merged_line[next_non_zero_ind]):
            merged_line[ref_pos] *= 2
            merged_line[next_non_zero_ind] = 0
            ref_pos = find_next_zero(merged_line, ref_pos + 1)
        else:
            next_zero_ind = find_next_zero(merged_line, ref_pos + 1)
            if(next_zero_ind != None and next_zero_ind < next_non_zero_ind):
                merged_line[next_zero_ind] = merged_line[next_non_zero_ind]
                merged_line[next_non_zero_ind] = 0
                ref_pos = next_zero_ind
            else:
                ref_pos = next_non_zero_ind
        next_non_zero_ind = find_next_non_zero(merged_line, ref_pos + 1)
    
    return merged_line

class TwentyFortyEight:
    """
    Class to run the game logic.
    """

    def __init__(self, grid_height, grid_width):
        # initialize the size of the grids
        self._height = grid_height
        self._width = grid_width
        # initialize the initial points at the 4 directions
        self._initials = {}
        self._initials[UP] = [[0, col] for col in range(self._width)]
        self._initials[DOWN] = [[self._height - 1, col] for col in range(self._width)]
        self._initials[LEFT] = [[row, 0] for row in range(self._height)]
        self._initials[RIGHT] = [[row, self._width - 1] for row in range(self._height)]
        # reset the grids
        self._grids = []
        self.reset()
        
    def reset(self):
        """
        Reset the game so the grid is empty except for two
        initial tiles.
        """
        # replace with your code
        self._grids = [[0 for dummy_col in range(self._width)] 
                          for dummy_row in range(self._height)]
        self.new_tile()
        self.new_tile()

    def __str__(self):
        """
        Return a string representation of the grid for debugging.
        """
        # replace with your code
        grids_list = []
        for row in range(self._height):
            grids_list.append(self._grids[row])
        return str(grids_list)

    def get_grid_height(self):
        """
        Get the height of the board.
        """
        # replace with your code
        return self._height

    def get_grid_width(self):
        """
        Get the width of the board.
        """
        # replace with your code
        return self._width

    def move(self, direction):
        """
        Move all tiles in the given direction and add
        a new tile if any tiles moved.
        """
        is_moved = False
        offset = OFFSETS[direction]
        # move each line in the designated direction sequentially
        for initial in self._initials[direction]:
            # retrieve the line
            line = []
            point = list(initial)
            while point[0] >= 0 and point[0] < self._height and point[1] >= 0 and point[1] < self._width:
                line.append(self.get_tile(point[0], point[1]))
                point[0] += offset[0]
                point[1] += offset[1]
            # move the line
            merged_line = merge(line)
            # update the line
            point = list(initial)
            for merged_ind in range(len(merged_line)):
                self.set_tile(point[0], point[1], merged_line[merged_ind])
                point[0] += offset[0]
                point[1] += offset[1]
                if not is_moved and line[merged_ind] != merged_line[merged_ind]:
                    is_moved = True
        if is_moved:
            self.new_tile()
            
    def new_tile(self):
        """
        Create a new tile in a randomly selected empty
        square.  The tile should be 2 90% of the time and
        4 10% of the time.
        """
        # randomly locate an empty cell
        rand_row = random.randrange(self._height)
        rand_col = random.randrange(self._width)
        while self.get_tile(rand_row, rand_col) != 0:
            rand_row = random.randrange(self._height)
            rand_col = random.randrange(self._width)
        
        # set the value of the located cell according 
        # to a uniform distribution
        if random.random() >= 0.1:
            self.set_tile(rand_row, rand_col, 2) # 90% of the time
        else:
            self.set_tile(rand_row, rand_col, 4) # 10% of the time

    def set_tile(self, row, col, value):
        """
        Set the tile at position row, col to have the given value.
        """
        # replace with your code
        self._grids[row][col] = value

    def get_tile(self, row, col):
        """
        Return the value of the tile at position row, col.
        """
        # replace with your code
        return self._grids[row][col]


# poc_2048_gui.run_gui(TwentyFortyEight(4, 4))
