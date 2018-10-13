# template for "Guess the number" mini-project
# input will come from buttons and an input field
# all output for the game will be printed in the console

import simplegui
import random
import math

low = 0
high = 100
base = 2
num_guess = int(math.ceil(math.log(high - low + 1, base)))
secret_number = random.randrange(low, high)

# helper function to start and restart the game
def new_game():
    # initialize global variables used in your code here
    global secret_number, num_guess 
    secret_number = random.randrange(low, high)
    num_guess = int(math.ceil(math.log(high - low + 1, base)))
    print ""
    print "New game. Range is from", low, " to ", high
    print "Number of remaining guesses is ", num_guess

# define event handlers for control panel
def range100():
    # button that changes the range to [0,100) and starts a new game 
    global low, high
    low = 0
    high = 100
    new_game()

def range1000():
    # button that changes the range to [0,1000) and starts a new game     
    global low, high
    low = 0
    high = 1000
    new_game()
    
def input_guess(guess):
    # main game logic goes here
    global num_guess
    guess_number = int(guess)
    print ""
    print "Guess was ", guess_number
    num_guess = num_guess - 1
    print "Number of remaining guesses is ", num_guess
    if(guess_number == secret_number):
        print("Correct!")
        new_game()
    elif(num_guess == 0):
        print "You ran out of guesses. The number was ", secret_number
        new_game()
    elif(guess_number < secret_number):
        print("Higher!")
    else:
        print("Lower!")

            
# create frame
frame = simplegui.create_frame("Guess the number", 200, 200);

# register event handlers for control elements and start frame
frame.add_button("Range is [0, 100)", range100, 200)
frame.add_button("Range is [0, 1000)", range1000, 200)
frame.add_input("Enter a guess", input_guess, 200)

# call new_game 
new_game()
frame.start()

# always remember to check your completed program against the grading rubric
