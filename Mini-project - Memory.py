# Mini-project #5 - Memory

import simplegui
import random

# import images
img1 = simplegui.load_image("https://dl.dropboxusercontent.com/u/25110163/Cat1.jpg")
img2 = simplegui.load_image("https://dl.dropboxusercontent.com/u/25110163/Cat2.jpg")
img3 = simplegui.load_image("https://dl.dropboxusercontent.com/u/25110163/Cat3.jpg")
img4 = simplegui.load_image("https://dl.dropboxusercontent.com/u/25110163/Cat4.jpg")
img5 = simplegui.load_image("https://dl.dropboxusercontent.com/u/25110163/Cat5.jpg")
img6 = simplegui.load_image("https://dl.dropboxusercontent.com/u/25110163/Cat6.jpg")
img7 = simplegui.load_image("https://dl.dropboxusercontent.com/u/25110163/Cat7.jpg")
img8 = simplegui.load_image("https://dl.dropboxusercontent.com/u/25110163/Cat8.jpg")

# global variables
cards = [img1, img2, img3, img4, img5, img6, img7, img8, 
         img1, img2, img3, img4, img5, img6, img7, img8]
exposed = []
state = 0
card1 = 0
card2 = 0
turns = 0

# helper function to initialize globals
def init():
    global state, card1, card2, turns, exposed
    
    random.shuffle(cards)
    exposed = []
    for i in range(0, 16):
        exposed.append(False)
        
    state = 0
    card1 = 0
    card2 = 0
    turns = 0
    
    label.set_text("Moves = " + str(turns))
        
# define event handlers
def mouseclick(pos):
    global card1, card2, state, turns
    
    if pos[1] < 100:
        card_num = pos[0] // 100
    else:
        card_num = (pos[0] // 100) + 8
    if state == 0:
        state = 1
        exposed[card_num] = True
        card1 = card_num
    elif state == 1 and not exposed[card_num]:
        state = 2
        exposed[card_num] = True
        card2 = card_num
        turns += 1
        label.set_text("Moves = " + str(turns))
    elif state ==2 and not exposed[card_num]:
        if cards[card1] != cards[card2]:    
            exposed[card1] = False
            exposed[card2] = False
        exposed[card_num] = True
        card1 = card_num
        state = 1
        
# cards are logically 50x100 pixels in size    
def draw(canvas):
    for i in range(1, 8):
        canvas.draw_line((i*100, 0), (i*100, 200), 2, "White")
    canvas.draw_line((0, 100), (800, 100), 2, "White")
    
    x = 50
    i = 0
    for card in cards:
        if exposed[i]:
            if i > 7:
                canvas.draw_image(card, (50, 50), (100, 100),
                                  (x-800, 150), (100, 100))                                  
            canvas.draw_image(card, (50, 50), (100, 100),
                              (x, 50), (100, 100))
        x += 100
        i += 1


# create frame and add a button and labels
frame = simplegui.create_frame("Memory", 800, 200)
frame.set_canvas_background("Black")
frame.add_button("Restart", init)
label = frame.add_label("Moves = 0")

# initialize global variables
init()

# register event handlers
frame.set_mouseclick_handler(mouseclick)
frame.set_draw_handler(draw)

# get things rolling
frame.start()
