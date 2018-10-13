# implementation of card game - Memory

import simplegui
import random

CARD_WIDTH = 50
CARD_HEIGHT = 100
NUM_CARDS = 8

cards = range(0, NUM_CARDS) + range(0, NUM_CARDS)
random.shuffle(cards)

exposed = []
for i in range(2 * NUM_CARDS):
    exposed.append(False)

state = 0

prev_card1 = 0
prev_card2 = 0

turns = 0

# helper function to initialize globals
def new_game():
    global state, turns
    state = 0
    turns = 0
    random.shuffle(cards)
    for i in range(2 * NUM_CARDS):
        exposed[i] = False
        
# define event handlers
def mouseclick(pos):
    # add game state logic here
    global state, prev_card1, prev_card2, turns
    card_ind = pos[0] // CARD_WIDTH
    if exposed[card_ind] == False: # ignores clicks on exposed cards
        if state == 0:
            turns += 1
            state = 1
            prev_card1 = card_ind
        elif state == 1:
            state = 2
            prev_card2 = card_ind
        else:
            if cards[prev_card1] != cards[prev_card2]:
                exposed[prev_card1] = False
                exposed[prev_card2] = False            
            turns += 1
            state = 1
            prev_card1 = card_ind
        exposed[card_ind] = True
                        
# cards are logically 50x100 pixels in size    
def draw(canvas):
    for card_ind in range(len(cards)):
        card_pos = card_ind * CARD_WIDTH
        if exposed[card_ind] == True:
            canvas.draw_text(str(cards[card_ind]), [card_pos, 7 * CARD_HEIGHT / 8], CARD_HEIGHT, "Red")
        else:
            card_lu = [card_pos, 0]
            card_ld = [card_pos, CARD_HEIGHT]
            card_rd = [card_pos + CARD_WIDTH - 1, CARD_HEIGHT]
            card_ru = [card_pos + CARD_WIDTH - 1, 0]
            canvas.draw_polygon([card_lu, card_ld, card_rd, card_ru], 2, "Black", "Green")
    label.set_text("Turns = " + str(turns))


# create frame and add a button and labels
frame = simplegui.create_frame("Memory", 800, 100)
frame.add_button("Reset", new_game)
label = frame.add_label("Turns = 0")

# register event handlers
frame.set_mouseclick_handler(mouseclick)
frame.set_draw_handler(draw)

# get things rolling
new_game()
frame.start()


# Always remember to review the grading rubric