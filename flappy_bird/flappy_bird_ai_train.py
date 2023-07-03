import pgzrun
import random
from bot import Bot
import pickle

TITLE = "Flappy Bird"
# Define the size of the game window
WIDTH = 400
HEIGHT = 708

GAP = 140 # Vertical distance between top and bottom pipes 
PIPE_SPEED = -3 #Pipe moving speed in pixels/frame
GRAVITY = 0.3
FLAP_STRENGTH = 9 # The number of pixels the bird would fly up, when keys are clicked. 
pipe_top = Actor("top",(WIDTH,0)) 
pipe_bottom = Actor("bottom",(WIDTH,pipe_top.height+GAP))

bird = Actor("bird1",(75,200))
bird.vy = 0 # Velocity of the bird
bird.dead = False
bird.score = 0
bird.highscore = 0

# The AI agent we are going to train to play the game
bot = Bot()

def draw():
    screen.blit("background",(0,0))
    pipe_top.draw()
    pipe_bottom.draw()
    bird.draw()
    screen.draw.text(
        str(bird.score),
        color='white',
        midtop =(WIDTH/2, 10),
        fontsize=70,
    )

    screen.draw.text(
        "Best: " + str(bird.highscore),
        color=(200, 170, 0),
        midbottom=(WIDTH/2, HEIGHT - 10),
        fontsize=30,
        shadow=(1, 1)
    )
        
def reset_pipes():
    random_position = random.randint(-150,150)
    pipe_top.midleft = (WIDTH, random_position)
    pipe_bottom.midleft = (WIDTH, random_position+pipe_top.height+GAP)
    
def on_key_down():
    if not bird.dead:
        bird.vy = -FLAP_STRENGTH
         
def update():
    update_bird()
    update_pipe()
    
def update_pipe():
    pipe_top.x += PIPE_SPEED
    pipe_bottom.x += PIPE_SPEED
    if pipe_top.right < 0:
        reset_pipes()
        if not bird.dead:
            bird.score +=1
            if bird.score >= bird.highscore:
                bird.highscore = bird.score
    
def update_bird():
    bird.y+=bird.vy
    bird.vy+=GRAVITY
    if not bird.dead:
        if bird.vy > 0:
            bird.image = "bird1"
        else:
            bird.image = "bird2"

        # Update AI agent's status using bird's horizontal distance to the pipe, vertical distance to bottom_pipe and the current velocity of the bird.
        status = bot.act(-bird.x + pipe_top.left,
             -bird.y + pipe_bottom.pos[1],
              bird.vy)
        if status==1: # click button if status==1 
            on_key_down()

    if bird.colliderect(pipe_top) or bird.colliderect(pipe_bottom):
        # Update score of the AI agent
        if not bird.dead:
            bot.update_scores()
            print("Game %d score %d" %  (bot.games, bird.score))
        bird.y = 200
        bird.dead = False
        bird.score = 0
        bird.vy = 0
        reset_pipes()

    if bird.y > HEIGHT or bird.y<=0:
        if not bird.dead:
            bot.update_scores()
            print("Game %d score %d" %  (bot.games, bird.score))
        bird.dead = False
        bird.y = 200
        bird.vy, bird.score = 0,0
        reset_pipes()



while True:
    update()
