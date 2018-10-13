"""
Implementation of hash table as lists of lists of tuples.
"""

import time

def create_ht(ht_size):
    """ 
    Returns an empty hash table of size ht_size.

    Arguments:
    ht_size - the length of the hash table

    Returns:
    A hash table containing ht_size empty chains (lists).
    """
    ht = []
    for dummy_idx in xrange(ht_size):
        ht.append([])
    return ht

def add_ht(ht, key, value):
    """
    Adds key/value pair to the hash table ht.
    If the key is already in the hash table, replace its old value with the new.
    
    Arguments:
    ht - the hash table
    key - the key of the key-value pair to store
    value - the value of the key-value pair to store
    """
    idx = hash(key) % len(ht)
    chain = ht[idx]
    for kvp in chain:
        if kvp[0] == key:
            chain.remove(kvp)
            break
    chain.append((key, value))
    

def remove_ht(ht, key):
    """
    Removes a key's value from the hash table.
    If no key is found in the table, no action is taken.
    
    Arguments:
    key - the key to search for in the hash table
    """  
    idx = hash(key) % len(ht)
    chain = ht[key]
    for kvp in chain:
        if kvp[0] == key:
            chain.remove(kvp)
            break
            
def lookup_ht(ht, key):
    """ 
    Returns the value associated with the key in the hash table ht.
    If the key is not present, raise an error.

    Returns:
    The value associated with the given key.
    """
    idx = hash(key) % len(ht)
    chain = ht[idx]
    for kvp in chain:
        if kvp[0] == key:
            return kvp[1]
    raise Exception("Key not found!")
    
def contains_key_ht(ht, key):
    """
    Tests whether a given key is contained in a hash table.

    Arguments:
    ht - the hash table
    key - the key to search for within the hash table

    Returns:
    True if the key is found, false otherwise.
    """
    idx = hash(key) % len(ht)
    chain = ht[idx]
    for kvp in chain:
        if kvp[0] == key:
            return True
    return False

def ht_test(n, size):
    """
    Computes search time for the nth element of hash table.

    Arguments:
    n - the number of elements in the table.
    size - the size (number of chains) of the table.

    Returns:
    The lookup time in seconds.
    """
    ht = create_ht(size)
    for i in xrange(n):
        add_ht(ht, i, i)
    start = time.clock()
    lookup_ht(ht, n - 1)
    stop = time.clock()
    return stop - start

def list_test(n):
    """
    Computes search time for the nth element of a list.

    Arguments:
    n - the number of elements in the list.

    Returns:
    The lookup time in seconds.
    """

    lst = []
    for i in xrange(n):
        lst.append(i)
    start = time.clock()
    lst.index(n - 1)
    stop = time.clock()
    return stop - start

def rehash_ht(ht, size):
    """
    Rehashes the given hash table in place to a new table size.

    Arguments:
    ht - the hash table to modify
    size - the new hash table size
    """
    kvps = set()
    while len(ht) > 0:
        chain = ht.pop()
        while len(chain) > 0:
            kvps.add(chain.pop())
    ht = create_ht(size)
    for i in xrange(size):
        ht.append([])
    for kvp in kvps:
        add_ht(ht, kvp[0], kvp[1])
        

if __name__ == '__main__':
    print ht_test(1000000, 100000)
    print list_test(1000000)
