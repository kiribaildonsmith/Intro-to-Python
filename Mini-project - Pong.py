# Mini-project #4 - Pong

import simplegui
import random

# initialize globals - pos and vel encode vertical info for paddles
WIDTH = 600
HEIGHT = 400       
BALL_RADIUS = 20
PAD_WIDTH = 8
PAD_HEIGHT = 80


# helper function that spawns a ball by updating the 
# ball's position vector and velocity vector
# if right is True, the ball's velocity is upper right, else upper left
def ball_init(right):
    global ball_pos, ball_vel # these are vectors stored as lists
    
    ball_pos = [WIDTH/2, HEIGHT/2]
    x = random.randint(120, 181)
    y = random.randint(40, 91)
    
    if right:
        ball_vel = [x/60, -(y/60)]
    else:
        ball_vel = [-(x/60), -(y/60)]

        
# helper function to calculate new, increased velocity
def inc_vel():
    global ball_vel
    
    if ball_vel[0] < 0:
        ball_vel[0] = round(ball_vel[0] + (ball_vel[0] * 0.1), 2)
    else:
        ball_vel[0] = round(ball_vel[0] + (ball_vel[0] * 0.1), 2)
        
    if ball_vel[1] < 0:
        ball_vel[1] = round(ball_vel[1] + (ball_vel[1] * 0.1), 2)
    else:
        ball_vel[1] = round(ball_vel[1] + (ball_vel[1] * 0.1), 2)
        
    ball_vel[0] = - ball_vel[0]
    
    
def new_game():
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel  # these are floats
    global score1, score2  # these are ints
    
    ball_init(True)
    
    paddle1_pos = HEIGHT/2
    paddle2_pos = HEIGHT/2
    paddle1_vel = 0
    paddle2_vel = 0
    
    score1 = 0
    score2 = 0

 
# define event handlers
def draw(c):
    global score1, score2, paddle1_pos, paddle2_pos, ball_pos, ball_vel
 
    # update paddle's vertical position, keep paddle on the screen
    if (paddle1_pos - PAD_HEIGHT/2 > 0) and (paddle1_vel < 0):
        paddle1_pos += paddle1_vel
    elif (paddle1_pos + PAD_HEIGHT/2 < HEIGHT) and (paddle1_vel > 0):
        paddle1_pos += paddle1_vel
    
    if (paddle2_pos - PAD_HEIGHT/2 > 0) and (paddle2_vel < 0):
        paddle2_pos += paddle2_vel
    elif (paddle2_pos + PAD_HEIGHT/2 < HEIGHT) and (paddle2_vel > 0):
        paddle2_pos += paddle2_vel
        
    # draw mid line and gutters
    c.draw_line([WIDTH / 2, 0],[WIDTH / 2, HEIGHT], 1, "White")
    c.draw_line([PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1, "White")
    c.draw_line([WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 1, "White")
    
    # draw paddles
    y1 = paddle1_pos + PAD_HEIGHT/2
    y2 = paddle1_pos - PAD_HEIGHT/2    
    c.draw_polygon([[0, y1], [0, y2], [8, y2], [8, y1]], 1, "White", "White") 

    y1 = paddle2_pos + PAD_HEIGHT/2
    y2 = paddle2_pos - PAD_HEIGHT/2    
    c.draw_polygon([[592, y1], [592, y2], [600, y2], [600, y1]], 1, "White", "White") 
     
    # update ball
    ball_pos[0] += ball_vel[0]
    ball_pos[1] += ball_vel[1]
    
    # ball bounces
    if ball_pos[0] <= BALL_RADIUS + 9:
        if (ball_pos[1] > paddle1_pos + PAD_HEIGHT/2) or (ball_pos[1] < paddle1_pos - PAD_HEIGHT/2):
            score2 += 1
            ball_init(True)
        else:
            inc_vel()
            #ball_vel[0] = - ball_vel[0]
    elif ball_pos[0] >= (WIDTH-9) - BALL_RADIUS:
        if (ball_pos[1] > paddle2_pos + PAD_HEIGHT/2) or (ball_pos[1] < paddle2_pos - PAD_HEIGHT/2):
            score1 += 1
            ball_init(False)
        else:
            inc_vel()
            #ball_vel[0] = - ball_vel[0]
    elif ball_pos[1] <= BALL_RADIUS:
        ball_vel[1] = - ball_vel[1]
    elif ball_pos[1] >= (HEIGHT-1) - BALL_RADIUS:
        ball_vel[1] = - ball_vel[1]
            
    # draw ball and scores
    c.draw_circle(ball_pos, BALL_RADIUS, 2, "White", "White")
    c.draw_text(str(score1), (150, 100), 52, "White")
    c.draw_text(str(score2), (450, 100), 52, "White")
        
        
def keydown(key):
    global paddle1_vel, paddle2_vel
    
    if key == simplegui.KEY_MAP["down"]:
        paddle2_vel = 4
    elif key == simplegui.KEY_MAP["up"]:
        paddle2_vel = -4
    elif key == simplegui.KEY_MAP["s"]:
        paddle1_vel = 4
    elif key == simplegui.KEY_MAP["w"]:
        paddle1_vel = -4
  
    
def keyup(key):
    global paddle1_vel, paddle2_vel

    if key == simplegui.KEY_MAP["down"]:
        paddle2_vel = 0
    elif key == simplegui.KEY_MAP["up"]:
        paddle2_vel = 0
    elif key == simplegui.KEY_MAP["s"]:
        paddle1_vel = 0
    elif key == simplegui.KEY_MAP["w"]:
        paddle1_vel = 0


def button_handler():
    score1 = 0
    score2 = 0
    
    new_game()
    
        
# create frame
f = simplegui.create_frame("Pong", WIDTH, HEIGHT)
f.set_draw_handler(draw)
f.set_keydown_handler(keydown)
f.set_keyup_handler(keyup)
f.add_button("Restart", button_handler)
f.add_label("Left-hand player W+S")
f.add_label("Right-hand player Up+Down")

# start frame
f.start()
new_game()