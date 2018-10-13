"""
Merge function for 2048 game.
"""

def slip_front(line):
    """
    Function that slips all the non-zero entries to the
    front of the line
    """
    
    # generate a line of zeros
    slip_line = []
    for line_index in range(len(line)):
        slip_line.append(0)
    
    # slip the line
    slip_index = 0
    for line_index in range(len(line)):
        if(line[line_index] != 0):
            slip_line[slip_index] = line[line_index]
            slip_index += 1
    
    # return the slip line
    return slip_line

def merge(line):
    """
    Function that merges a single row or column in 2048.
    """
    # slip all non-zero entries to front end
    result_line = slip_front(line)
    
    # merge the line
    for result_index in range(len(result_line) - 1):
        if(result_line[result_index] == result_line[result_index + 1]):
            result_line[result_index] = 2 * result_line[result_index]
            result_line[result_index + 1] = 0
            result_index += 1
    
    # slip front and return the result line
    return slip_front(result_line)

# tests
# line = [8, 16, 16, 8]
# print merge(line)