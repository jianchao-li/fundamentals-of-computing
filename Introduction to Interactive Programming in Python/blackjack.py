# Mini-project #6 - Blackjack

import simplegui
import random


# load card sprite - 936x384 - source: jfitz.com
CARD_SIZE = (72, 96)
CARD_CENTER = (36, 48)
card_images = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/cards_jfitz.png")

CARD_BACK_SIZE = (72, 96)
CARD_BACK_CENTER = (36, 48)
card_back = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/card_jfitz_back.png")    

CARD_GAP = 10


# initialize some useful global variables
in_play = False
game_over = True

outcome = ""
result = ""

WIN_MESSAGE = "Congratulations! You win!"
LOSE_MESSAGE = "Sorry... You lose..."
STOP_MESSAGE = "You stop a game and lose..."

score = 0

hints_l1 = 'HINTS: Once you start the game or click "deal", a new game'
hints_l2 = 'is on and you cannot click "deal" again immediately;'
hints_l3 = "otherwise, you stop an in-play game and the system assumes"
hints_l4 = 'you to lose. Once you win or lose, you can click "deal" to'
hints_l5 = "start a new game. Have fun :)"

# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}


# define card class
class Card:
    def __init__(self, suit, rank):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
        else:
            self.suit = None
            self.rank = None
            print "Invalid card: ", suit, rank

    def __str__(self):
        return self.suit + self.rank

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

    def draw(self, canvas, pos):
        card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank), 
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
        canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)

        
# define hand class
class Hand:
    def __init__(self):
        # create Hand object
        self.cards = []

    def __str__(self):
        # return a string representation of a hand
        hand_info = "Hand contains "
        for card in self.cards:
            hand_info += (str(card) + ' ')
        return hand_info

    def add_card(self, card):
        # add a card object to a hand
        self.cards.append(card)

    def get_value(self):
        # count aces as 1, if the hand has an ace, then add 10 to hand value if it doesn't bust
        # compute the value of the hand, see Blackjack video
        value = 0
        has_aces = False
        for card in self.cards:
            value += VALUES[card.rank]
            if card.rank == 'A':
                has_aces = True
        if has_aces:
            if value + 10 <= 21:
                return value + 10
            else:
                return value
        else:
            return value
    
    def hit(self, card):
        # hit the hand
        self.cards.append(card)
    
    def draw(self, canvas, pos):
        # draw a hand on the canvas, use the draw method for cards
        temp_pos = list(pos)
        for card in self.cards:
            card.draw(canvas, temp_pos)
            temp_pos[0] += (CARD_SIZE[0] + CARD_GAP)
 
        
# define deck class 
class Deck:
    def __init__(self):
        # create a Deck object
        self.cards = []
        for suit in SUITS:
            for rank in RANKS:
                self.cards.append(Card(suit, rank))

    def shuffle(self):
        # shuffle the deck 
        # use random.shuffle()
        random.shuffle(self.cards)
        
    def deal_card(self):
        # deal a card object from the deck
        card = self.cards[-1]
        self.cards.pop(-1)
        return card
    
    def __str__(self):
        # return a string representing the deck
        deck_info = "Deck contains "
        for card in self.cards:
            deck_info += (str(card) + ' ')
        return deck_info

    
# define globals for game
deck = Deck()
player_hand = Hand()
dealer_hand = Hand()


#define event handlers for buttons
def deal():
    global outcome, in_play, player_hand, dealer_hand, player_pos, dealer_pos, result, game_over, score
    
    # create and shuffle a new deck
    deck = Deck()
    deck.shuffle()
    
    # create hands for players and dealers
    player_hand = Hand()
    dealer_hand = Hand()
    
    # add cards to player's hands
    player_hand.add_card(deck.deal_card())
    player_hand.add_card(deck.deal_card())
    
    # add cards to dealer's hands
    dealer_hand.add_card(deck.deal_card())
    dealer_hand.add_card(deck.deal_card())
    
    # define player and dealer's positions for their cards
    player_pos = [120, 302]
    dealer_pos = [120, 102]
    
    # the trickiest part of the logic inside deal()
    if not game_over:
        # player loses if he stops an in-play game
        score -= 1
        result = STOP_MESSAGE
        outcome = "New deal?"
        in_play = False
        game_over = True
    else:
        # simply starts a new game
        result = ""
        outcome = "Hit or stand?"
        in_play = True
        game_over = False

        
def hit():
    # replace with your code below
    global in_play, player_hand, dealer_hand, score, outcome, result, game_over
    
    # if the hand is in play, hit the player
    if not game_over:
        if in_play:
            # hit the player
            player_hand.hit(deck.deal_card())
        else:
            # hit the dealer
            dealer_hand.hit(deck.deal_card())
   
    # if busted, assign a message to outcome, update in_play and score
    if not game_over:
        if in_play:
            # check for the player's value of hand
            player_value = player_hand.get_value()
            if player_value > 21:
                score -= 1
                result = LOSE_MESSAGE
                outcome = "New deal?"
                in_play = False
                game_over = True
        else:
            # check for the dealer's value of hand
            dealer_value = dealer_hand.get_value()
            if dealer_value > 21:
                score += 1
                result = WIN_MESSAGE
                outcome = "New deal?"
                game_over = True


def stand():
    # replace with your code below
    global in_play, player_hand, dealer_hand, score, outcome, result, game_over
    
    # if hand is in play, repeatedly hit dealer until his hand has value 17 or more
    if not game_over:
        if in_play:
            # switch hit from player to dealer by changing in_play
            in_play = False
            while dealer_hand.get_value() < 17:
                hit()

    # assign a message to outcome, update in_play and score
    if not game_over:
        # dealer wins ties in this version
        if dealer_hand.get_value() < player_hand.get_value():
            result = WIN_MESSAGE
            score += 1
        else:
            result = LOSE_MESSAGE
            score -= 1
        game_over = True
        # in_play has been set to be False in above statements

        
# draw handler    
def draw(canvas):
    # test to make sure that card.draw works, replace with your code below
    
    global outcome, score, in_play, player_pos, dealer_pos, result, hints
    
    # draw player's hand of cards
    pos = list(player_pos)
    player_hand.draw(canvas, player_pos)
    
    # draw dealer's hand of cards
    dealer_hand.draw(canvas, dealer_pos)
    if in_play:
        pos = list(dealer_pos)
        canvas.draw_image(card_back, CARD_BACK_CENTER, CARD_BACK_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_BACK_SIZE)
        pos[0] += (CARD_SIZE[0] + CARD_GAP)
        dealer_hand.cards[1].draw(canvas, pos)
        
    # draw game information
    canvas.draw_text("Blackjack", (200, 50), 50, "Orange")
    canvas.draw_text("Player", (30, 350), 25, "Yellow")
    canvas.draw_text("Dealer", (30, 150), 25, "Yellow")
    canvas.draw_text(outcome, (390, 260), 30, "Lime")
    if result == WIN_MESSAGE:
        canvas.draw_text(result, (50, 450), 40, "Red")
    else:
        canvas.draw_text(result, (50, 450), 40, "Purple")
    canvas.draw_text("Score " + str(score), (460, 80), 30, "Aqua")
    canvas.draw_text(hints_l1, (5, 510), 20, "White")
    canvas.draw_text(hints_l2, (5, 530), 20, "White")
    canvas.draw_text(hints_l3, (5, 550), 20, "White")
    canvas.draw_text(hints_l4, (5, 570), 20, "White")
    canvas.draw_text(hints_l5, (5, 590), 20, "White")
    
# initialization frame
frame = simplegui.create_frame("Blackjack", 600, 600)
frame.set_canvas_background("Green")


#create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
frame.set_draw_handler(draw)


# get things rolling
deal()
frame.start()


# remember to review the gradic rubric