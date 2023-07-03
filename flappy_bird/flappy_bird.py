import pgzrun
import random

TITLE = "Flappy Bird"
WIDTH = 400
HEIGHT = 708

GAP = 140 #green
PIPE_SPEED = -3 #green
GRAVITY = 0.3
FLAP_STRENGTH = 9
top = Actor("top",(WIDTH,0)) #blue
bottom = Actor("bottom",(WIDTH,top.height+GAP))  #blue

bird = Actor("bird1",(75,200))
bird.vy = 0
bird.dead = False

bird.score = 0
bird.highscore = 0

def draw():
    screen.blit("background",(0,0))
    top.draw()
    bottom.draw()
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
    top.midleft = (WIDTH, random_position)
    bottom.midleft = (WIDTH, random_position+top.height+GAP)
    
def on_key_down():
    if not bird.dead:
        bird.vy = -FLAP_STRENGTH
         
def update():
    update_bird()
    update_pipe()
    
def update_pipe():
    top.x += PIPE_SPEED
    bottom.x += PIPE_SPEED
    if top.right < 0:
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
    if bird.colliderect(top) or bird.colliderect(bottom):
        bird.dead = True
        bird.image = "birddead"
    if bird.y > HEIGHT:
        bird.dead = False
        bird.y = 200
        bird.vy, bird.score = 0,0
        reset_pipes()


pgzrun.go()