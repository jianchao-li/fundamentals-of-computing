"""
A simple recursive solver for Nim
http://en.wikipedia.org/wiki/Nim#The_21_game
"""

INITIAL_NUM = 21
MAX_REMOVE = 3

# recursive solver with no memoization


def evaluate_position(current_num):
    """
    Recursive solver for Nim
    """
    global counter
    counter += 1

    # enter code here
    for remove_num in range(1, min(MAX_REMOVE + 1, current_num + 1)):
        if evaluate_position(current_num - remove_num) == "lost":
            return "won"
    return "lost"

def run_standard(items):
    """
    Encapsulate code to run regular recursive solver
    """
    global counter
    counter = 0
    print
    print "Standard recursive version"
    print "Position with", items, "items is", evaluate_position(items)
    print "Evaluated in", counter, "calls"

run_standard(INITIAL_NUM)


# memoized version with dictionary

def evaluate_memo_position(current_num, memo_dict):
    """
    Memoized version of evaluate_position
    memo_dict is a dictionary that stores previously computed results
    """
    global counter
    counter += 1

    # enter code here
    for remove_num in range(1, min(MAX_REMOVE + 1, current_num + 1)):
        new_num = current_num - remove_num
        if memo_dict.has_key(new_num):
            if memo_dict[new_num] == "lost":
                memo_dict[current_num] = "won"
                return "won"
        else:
            if evaluate_memo_position(new_num, memo_dict) == "lost":
                memo_dict[current_num] = "won"
                return "won"
    memo_dict[current_num] = "lost"
    return "lost"


def run_memoized(items):
    """
    Run the memoized version of the solver
    """
    global counter
    counter = 0
    print
    print "Memoized version"
    print "Position with", items, "items is", evaluate_memo_position(items, {0 : "lost"})
    print "Evaluated in", counter, "calls"
    
run_memoized(INITIAL_NUM)
