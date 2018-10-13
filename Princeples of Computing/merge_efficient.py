"""
Merge function for 2048 game.
"""

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
    Function that merges a single row or column in 2048.
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