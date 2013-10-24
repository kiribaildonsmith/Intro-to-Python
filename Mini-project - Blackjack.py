# Mini-project #6 - Blackjack

import simplegui
import random


# load card sprite - 949x392 - source: jfitz.com
CARD_SIZE = (73, 98)
CARD_CENTER = (36.5, 49)
card_images = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/cards.jfitz.png")

CARD_BACK_SIZE = (71, 96)
CARD_BACK_CENTER = (35.5, 48)
card_back = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/card_back.png")    


# initialize some useful global variables
in_play = False
outcome = ""
dealer_mess = ""
player_mess = ""
score_mess = "Score: 0"
score = 0


# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9,
          'T':10, 'J':10, 'Q':10, 'K':10}


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
        canvas.draw_image(card_images, card_loc, CARD_SIZE,
                          [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]],
                          CARD_SIZE)
        
        
# define hand class
class Hand:
    def __init__(self):
        self.cards = []

    def __str__(self):
        s = "Hand contains"
        for c in self.cards:
            s = s + " " + str(c)
        return s

    def add_card(self, card):
        # add a card object to a hand
        self.cards.append(card)	

    def get_value(self):
        # count aces as 1, if the hand has an ace, then add 10 to hand 
        # value if it doesn't bust
        i = 0
        for c in self.cards:
            i += VALUES[c.rank]
        # dealing with aces
        for c in self.cards:
            if RANKS.index(c.rank) == 0 and i < 12:
                i += 10
        return i        
   
    def draw(self, canvas, pos):
        # draw a hand on the canvas, use the draw method for cards
        i = 0
        for c in self.cards:
            current = (pos[0] + i, pos[1])
            c.draw(canvas, current)
            i += 80
 
        
# define deck class 
class Deck:
    def __init__(self):
        # create a Deck object
        self.cards = []	
        self.dealt = []
        for s in SUITS:
            for r in RANKS:
                c = Card(s, r)
                self.cards.append(c)

    def shuffle(self):
        # add cards back to deck and shuffle
        if self.dealt != []:
            for c in self.dealt:
                self.cards.append(c)
            
        random.shuffle(self.cards)

    def deal_card(self):
        # deal a card object from the deck
        c = self.cards.pop()
        self.dealt.append(c)
        
        return c
    
    def __str__(self):
        # return a string representing the deck
        s = "Deck contains"
        for c in self.cards:
            s = s + " " + str(c)
        return s


#define event handlers for buttons
def deal():
    global outcome, in_play, player, dealer, score
    global dealer_mess, player_mess, score_mess

    if in_play:
        outcome = "Dealer wins. Cannot redeal during play"
        score -= 1
        score_mess = "Score: " + str(score)
        
    deck.shuffle()
    
    # deal player's initial hand
    player = Hand()
    player.add_card(deck.deal_card())
    player.add_card(deck.deal_card())
    
    # deal dealer's initial hand
    dealer = Hand()
    dealer.add_card(deck.deal_card())
    dealer.add_card(deck.deal_card())
    
    in_play = True
    outcome = "Hit or stand?"
    dealer_mess = ""
    player_mess = ""
    
    
def hit():
    global in_play, player, score, outcome, score_mess
 
    # if the hand is in play, hit the player
    if in_play and player.get_value() < 22:
        player.add_card(deck.deal_card())
    
    # if busted, assign a message to outcome, update in_play and score    
    if player.get_value() > 21:
        in_play = False
        outcome =  "You have busted."
        score -= 1
        score_mess = "Score: " + str(score)
    
    
def stand():
    global in_play, player, dealer, score, outcome
    global dealer_mess, player_mess, score_mess
   
    # if hand is in play, repeatedly hit dealer until
    # his hand has value 17 or more
    if in_play:
        while dealer.get_value() < 17:
            dealer.add_card(deck.deal_card())
        
        # assign a message to outcome, update in_play and score
        if dealer.get_value() > 21:
            outcome =  "Dealer has busted. You win!"
            score += 1
        elif dealer.get_value() >= player.get_value():
            outcome = "Dealer wins"
            score -= 1
        else:
            outcome =  "You win"
            score += 1
            
        dealer_mess = "Dealer's value: " + str(dealer.get_value())
        player_mess = "Player's value: " + str(player.get_value())
        score_mess =  "Score: " + str(score)
        
        in_play = False
    else:
        outcome = "You have already busted."        
    

# draw handler    
def draw(canvas):
    
    canvas.draw_text("Blackjack", (200, 50), 48, "Black", "sans-serif")    
    canvas.draw_text(outcome, (200, 320), 16, "Black", "sans-serif")
    canvas.draw_text(score_mess, (200, 340), 16, "Black", "sans-serif")
    canvas.draw_text(player_mess, (200, 360), 16, "Black", "sans-serif")
    canvas.draw_text(dealer_mess, (200, 380), 16, "Black", "sans-serif")
    
    player.draw(canvas, (100, 480))
    dealer.draw(canvas, (100, 120))
    
    # cover dealer's hole card while in play
    if in_play:
        canvas.draw_image(card_back, CARD_BACK_CENTER, CARD_BACK_SIZE, 
                          (100 + CARD_BACK_CENTER[0], 120 + CARD_BACK_CENTER[1]),
                           CARD_BACK_SIZE)       

       

# initialization frame
frame = simplegui.create_frame("Blackjack", 600, 600)
frame.set_canvas_background("Green")


#create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
frame.set_draw_handler(draw)


# get things rolling
player = Hand()
dealer = Hand()
deck = Deck()
outcome = "New deal?"
frame.start()