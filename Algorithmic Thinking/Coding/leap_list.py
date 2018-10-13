def is_goal_reachable_max(leap_list, start_index, max_leaps):
    """ 
    Determines whether goal can be reached in at most max_leaps leaps.

    Arguments:
    leap_list - the leap list game board.
    start_index - the starting index of the player.
    max_leaps - the most number of leaps allowed before the player loses.

    Returns:
    True if goal is reachable in max_leap or less leaps.  False if goal is not reachable in max_leap or fewer leaps.
    """
    if leap_list[start_index] == 0:
        return True
    if max_leaps == 0:
        return False
    leap_left_index = start_index - leap_list[start_index]
    leap_right_index = start_index + leap_list[start_index]
    if leap_left_index >= 0 and is_goal_reachable_max(leap_list, leap_left_index, max_leaps - 1):
        return True
    if leap_right_index < len(leap_list) and is_goal_reachable_max(leap_list, leap_right_index, max_leaps - 1):
        return True
    return False
    
print is_goal_reachable_max([1, 2, 3, 3, 3, 1, 0], 0, 3)
print is_goal_reachable_max([1, 2, 3, 3, 3, 1, 0], 0, 2)
print is_goal_reachable_max([1, 2, 3, 3, 3, 1, 0], 4, 3)
print is_goal_reachable_max([1, 2, 3, 3, 3, 1, 0], 4, 2)
print is_goal_reachable_max([2, 1, 2, 2, 2, 0], 1, 5)
print is_goal_reachable_max([2, 1, 2, 2, 2, 0], 3, 1)

def is_goal_reachable_helper(leap_list, start_index, visited):
    """
    Helper function fo is_goal_reachable()
    """
    if leap_list[start_index] == 0:
        return True
    visited.add(start_index)
    leap_left_index = start_index - leap_list[start_index]
    leap_right_index = start_index + leap_list[start_index]    
    if leap_left_index >= 0 and not leap_left_index in visited and is_goal_reachable_helper(leap_list, leap_left_index, visited):
        return True
    if leap_right_index < len(leap_list) and not leap_right_index in visited and is_goal_reachable_helper(leap_list, leap_right_index, visited):
        return True
    return False

def is_goal_reachable(leap_list, start_index):
    """ 
    Determines whether goal can be reached in any number of leaps.

    Arguments:
    leap_list - the leap list game board.
    start_index - the starting index of the player.

    Returns:
    True if goal is reachable.  False if goal is not reachable.
    """
    visited = set()
    return is_goal_reachable_helper(leap_list, start_index, visited)

print is_goal_reachable([1, 2, 3, 3, 3, 1, 0], 0)
print is_goal_reachable([1, 2, 3, 3, 3, 1, 0], 4)
print is_goal_reachable([2, 1, 2, 2, 2, 0], 1)
print is_goal_reachable([2, 1, 2, 2, 2, 0], 3)
print is_goal_reachable([3, 6, 4, 1, 3, 4, 2, 5, 3, 0], 0)