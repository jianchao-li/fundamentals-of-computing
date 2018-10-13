"""
Write a function to plot the distribution
of the sum of two dice for a given number of rolls.
"""

import random
import matplotlib.pyplot as plt

NROLLS = 10000

def roll_dice():
    """
    Roll a dice.
    """
    return random.randrange(1, 7)

def plot_dice_rolls(nrolls):
    """
    Plot the distribution of the sum of two dice when they are rolled
    nroll times.

    Arguments:
    nrolls - the number of times to roll the pair of dice

    Returns:
    Nothing
    """
    distribution = {}
    for dummy_idx in range(nrolls):
        dice1 = roll_dice()
        dice2 = roll_dice()
        dsum = dice1 + dice2
        if dsum in distribution.keys():
            distribution[dsum] += 1
        else:
            distribution[dsum] = 1
    for dsum in distribution.keys():
        distribution[dsum] /= float(nrolls)
    plt.plot(distribution.keys(), distribution.values(), 'g^')
    plt.grid(True)
    plt.xlabel("Sum of Dice Rolls")
    plt.ylabel("Frequency of Ocurrence")
    plt.title("Distribution Plot of Sum of Two Dice Rolls")
    plt.show()

if __name__ == "__main__":
    plot_dice_rolls(NROLLS)
    
