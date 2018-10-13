"""
Student code for Word Wrangler game
"""

import urllib2
import codeskulptor
import poc_wrangler_provided as provided

WORDFILE = "assets_scrabble_words3.txt"


# Functions to manipulate ordered word lists

def remove_duplicates(list1):
    """
    Eliminate duplicates in a sorted list.

    Returns a new sorted list with the same elements in list1, but
    with no duplicates.

    This function can be iterative.
    """
    new_list = []
    for ind in range(len(list1)):
        if len(new_list) == 0 or list1[ind] != list1[ind - 1]:
            new_list.append(list1[ind])
    return new_list

def intersect(list1, list2):
    """
    Compute the intersection of two sorted lists.

    Returns a new sorted list containing only elements that are in
    both list1 and list2.

    This function can be iterative.
    """
    new_list = []
    list1_remove = remove_duplicates(list1)
    list2_remove = remove_duplicates(list2)
    ind1 = 0
    ind2 = 0
    while ind1 < len(list1_remove) and ind2 < len(list2_remove):
        if list1_remove[ind1] == list2_remove[ind2]:
            new_list.append(list1_remove[ind1])
            ind1 += 1
            ind2 += 1
        elif list1_remove[ind1] < list2_remove[ind2]:
            ind1 += 1
        else:
            ind2 += 1
    return new_list

# Functions to perform merge sort

def merge(list1, list2):
    """
    Merge two sorted lists.

    Returns a new sorted list containing all of the elements that
    are in either list1 and list2.

    This function can be iterative.
    """
    ind1 = 0
    ind2 = 0
    merged_list = []
    while ind1 < len(list1) and ind2 < len(list2):
        if list1[ind1] <= list2[ind2]:
            merged_list.append(list1[ind1])
            ind1 += 1
        else:
            merged_list.append(list2[ind2])
            ind2 += 1
    while ind1 < len(list1):
        merged_list.append(list1[ind1])
        ind1 += 1
    while ind2 < len(list2):
        merged_list.append(list2[ind2])
        ind2 += 1
    return merged_list

def merge_sort(list1):
    """
    Sort the elements of list1.

    Return a new sorted list with the same elements as list1.

    This function should be recursive.
    """
    if len(list1) <= 1:
        return list1
    else:
        mid = len(list1) // 2
        left_half = merge_sort(list1[0 : mid])
        right_half = merge_sort(list1[mid : ])
        return merge(left_half, right_half)

# Function to generate all strings for the word wrangler game

def gen_all_strings(word):
    """
    Generate all strings that can be composed from the letters in word
    in any order.

    Returns a list of all strings that can be formed from the letters
    in word.

    This function should be recursive.
    """
    if len(word) == 0:
        return [""]
    else:
        first = word[0]
        rest = word[1:]
        rest_strings = gen_all_strings(rest)
        new_strings = []
        for string in rest_strings:
            if len(string) == 0:
                new_strings.append(first)
            else:
                new_strings.append(first + string)
                for ind in range(1, len(string)):
                    new_strings.append(string[:ind] + first + string[ind:])
                new_strings.append(string + first)
        return rest_strings + new_strings
    
# Function to load words from a file

def load_words(filename):
    """
    Load word list from the file named filename.

    Returns a list of strings.
    """
    url = codeskulptor.file2url(filename)
    netfile = urllib2.urlopen(url)
    dictionary = []
    for line in netfile.readlines():
        dictionary.append(line[0:-1])   
    return dictionary

def run():
    """
    Run game.
    """
    words = load_words(WORDFILE)
    wrangler = provided.WordWrangler(words, remove_duplicates, 
                                     intersect, merge_sort, 
                                     gen_all_strings)
    provided.run_game(wrangler)

# Uncomment when you are ready to try the game
# run()

    
    
