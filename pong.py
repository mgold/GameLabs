import pygame, sys
from pygame.constants import *
from Paddle import Paddle
from Puck import Puck
from math import atan2, sin, cos

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
MATCH_LENGTH = 11
GOAL_WIDTH = 5
RED = (255, 0, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
CONTROLS1 = [K_w, K_a, K_s, K_d]
CONTROLS2 = [K_UP, K_DOWN, K_LEFT, K_RIGHT]

def render():
    # Clear screen
    screen.fill(WHITE)
    for i in range(20):
        pygame.draw.rect(screen, RED, pygame.Rect((SCREEN_WIDTH/2 -3, 60*i+15), (6,30)))
    pygame.draw.rect(screen, BLUE, midline1_rect)
    pygame.draw.rect(screen, BLUE, midline2_rect)
    pygame.draw.rect(screen, BLACK,   edge1_rect)
    pygame.draw.rect(screen, BLUE, goal1_rect)
    pygame.draw.rect(screen, BLACK,   edge2_rect)
    pygame.draw.rect(screen, RED, goal2_rect)
   
    #Precomputed for performance (yes, it was noticeable)
    pygame.draw.circle(screen, RED, (150, 150), 15)
    pygame.draw.circle(screen, RED, (150, 150), 80, 10)
    pygame.draw.circle(screen, RED, (150, 450), 15)
    pygame.draw.circle(screen, RED, (150, 450), 80, 10)
    pygame.draw.circle(screen, RED, (650, 150), 15)
    pygame.draw.circle(screen, RED, (650, 150), 80, 10)
    pygame.draw.circle(screen, RED, (650, 450), 15)
    pygame.draw.circle(screen, RED, (650, 450), 80, 10)
    pygame.draw.circle(screen, WHITE, (400, 300), 90)
    pygame.draw.circle(screen, RED, (400, 300), 10)
    pygame.draw.circle(screen, RED, (400, 300), 90, 10)

    # Render the ball and paddles
    puck.draw()
    paddle1.draw()
    paddle2.draw()

    # Render the scores
    score1_text = font.render(str(score1), True, BLUE)
    screen.blit(score1_text, (150 - font.size(str(score1))[0] / 2, 5)) # The score1
    score2_text = font.render(str(score2), True, RED)
    screen.blit(score2_text, (650  - font.size(str(score2))[0] / 2, 5)) # The score2


def win(victor, color):
    render()

    win_text = winFont.render(str(victor+" wins!"), True, color)
    screen.blit(win_text, (280, SCREEN_HEIGHT/2))
                        #Calculating x not working for some reason

    rematch_text = font.render(str("Press any key to play again"), True, (0,0,0))
    screen.blit(rematch_text, ((SCREEN_WIDTH / 2) - font.size(str(rematch_text))[0] / 2, SCREEN_HEIGHT/2 + 50))

    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):  
                sys.exit(0)
                pygame.quit()
            elif event.type == pygame.KEYDOWN:
                score1 = score2 = 0
                return

def collide (puck, paddle):
    #Ignoring factor of pi/2
    momentumx = (puck.area * puck.dx**2) + (paddle.area * paddle.dx**2)
    puck.dx = (momentumx/puck.area)**.5
    momentumy = (puck.area * puck.dy**2) + (paddle.area * paddle.dy**2)
    puck.dx = (momentumy/puck.area)**.5
    paddle.dx = paddle.dy = 0
    boing.play()

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Pong")

try:
    boing = pygame.mixer.Sound("boing.wav")
    thunk = pygame.mixer.Sound("thunk.wav")
    goal  = pygame.mixer.Sound("goal.wav")
except pygame.error:
    print "Sounds could not be loaded."
    quit();

puck = Puck(screen, SCREEN_WIDTH//2, SCREEN_HEIGHT//2)

paddle1 = Paddle(screen, GOAL_WIDTH, 300, BLUE)
paddle2 = Paddle(screen, 500, SCREEN_WIDTH - GOAL_WIDTH, RED)

edge1_rect = pygame.Rect((0, 0), (GOAL_WIDTH, SCREEN_HEIGHT))
goal1_rect = pygame.Rect((0, (3.0/8)*SCREEN_HEIGHT), (GOAL_WIDTH, (1.0/4)*SCREEN_HEIGHT))
edge2_rect = pygame.Rect((SCREEN_WIDTH-GOAL_WIDTH, 0), (GOAL_WIDTH, SCREEN_HEIGHT))
goal2_rect = pygame.Rect((SCREEN_WIDTH-GOAL_WIDTH, (3.0/8)*SCREEN_HEIGHT), (GOAL_WIDTH, (1.0/4)*SCREEN_HEIGHT))
midline1_rect = pygame.Rect((300, 0), (3, SCREEN_HEIGHT))
midline2_rect = pygame.Rect((500, 0), (3, SCREEN_HEIGHT))

score1 = 0
score2 = 0

# Load the font for displaying the score and game result
font = pygame.font.Font(None, 30)
winFont = pygame.font.Font(None, 72)

commands = []

# Game loop
while True:
    sleeptime = 0
    
    # Event handler
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit(0)
            pygame.quit()
        elif event.type == pygame.KEYDOWN:
            if event.key == K_ESCAPE:
                sys.exit(0)
                pygame.quit()
            else:
                commands.append(event.key)
        elif event.type == KEYUP:
            try:
                commands.remove(event.key)
            except:
                pass

    paddle1.update(filter(lambda c: c in CONTROLS1, commands))
    paddle2.update(filter(lambda c: c in CONTROLS2, commands))  

    # Update ball position

    puck.update()

    # Puck collision with top and bottom
    if puck.y <= 0 or puck.y  >= SCREEN_HEIGHT:
        puck.collidey()
        thunk.play()
    #Right goal - player 1 score
    elif goal2_rect.colliderect(puck.rect):
        goal.play()
        puck.reset()
        score1 += 1
        if score1 == MATCH_LENGTH:
            win("Blue", BLUE)
            score1 = score2 = 0
        else:
            sleeptime += 1
    #Left goal - player 2 score
    elif goal1_rect.colliderect(puck.rect):
        goal.play()
        puck.reset()
        score2 +=1
        if score2 == MATCH_LENGTH:
            win("Red", RED)
            score1 = score2 = 0
        else:
            sleeptime += 1
    #Ball collision with non-goal sides
    elif puck.rect.colliderect(edge1_rect) or puck.rect.colliderect(edge2_rect):
        puck.collidex()
        thunk.play()
     #Paddle collision - reverse speed
    elif pygame.sprite.collide_circle(paddle1, puck):
        collide(puck, paddle1)
    elif pygame.sprite.collide_circle(puck, paddle2):
        collide(puck, paddle2)

    render()

    # Update screen and wait 20 milliseconds
    pygame.display.flip()
    pygame.time.delay(1000*sleeptime)
    pygame.time.delay(20)
