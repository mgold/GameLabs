import pygame, sys
from pygame.constants import *
from Paddle import Paddle

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
PADDLE1_START_X = 10
PADDLE1_START_Y = 20
PADDLE2_START_X = 780
PADDLE2_START_Y = 20
PADDLE_WIDTH = 10
PADDLE_HEIGHT = 80
BALL_SPEED = 10
PADDLE_SPEED = BALL_SPEED * 1.5
BALL_WIDTH_HEIGHT = 32
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
    pygame.draw.circle(screen, BLACK, ball_rect.center, ball_rect.width / 2) # The ball
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

# This is a rect that contains the ball at the beginning it is set in the center of the screen
ball_rect = pygame.Rect((SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2), (BALL_WIDTH_HEIGHT, BALL_WIDTH_HEIGHT))

# Speed of the ball (x, y)
ball_speed = [BALL_SPEED, BALL_SPEED]

paddle1 = Paddle(screen, GOAL_WIDTH, 300, BLUE)
paddle2 = Paddle(screen, 500, SCREEN_WIDTH - GOAL_WIDTH, RED)

edge1_rect = pygame.Rect((0, 0), (GOAL_WIDTH, SCREEN_HEIGHT))
goal1_rect = pygame.Rect((0, (3.0/8)*SCREEN_HEIGHT), (GOAL_WIDTH, (1.0/4)*SCREEN_HEIGHT))
edge2_rect = pygame.Rect((SCREEN_WIDTH-GOAL_WIDTH, 0), (GOAL_WIDTH, SCREEN_HEIGHT))
goal2_rect = pygame.Rect((SCREEN_WIDTH-GOAL_WIDTH, (3.0/8)*SCREEN_HEIGHT), (GOAL_WIDTH, (1.0/4)*SCREEN_HEIGHT))
midline1_rect = pygame.Rect((300, 0), (3, SCREEN_HEIGHT))
midline2_rect = pygame.Rect((500, 0), (3, SCREEN_HEIGHT))

# Scoring: 1 point if you hit the ball, -5 point if you miss the ball
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
    ball_rect.left += ball_speed[0]
    ball_rect.top += ball_speed[1]

    # Ball collision with top and bottom
    if ball_rect.top <= 0 or ball_rect.bottom >= SCREEN_HEIGHT:
        ball_speed[1] = -ball_speed[1]
        thunk.play()
    #Right goal - player 1 score
    elif ball_rect.colliderect(goal2_rect):
        goal.play()
        ball_speed[0] = BALL_SPEED
        ball_rect.center = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
        score1 += 1
        if score1 == MATCH_LENGTH:
            win("Blue", BLUE)
            score1 = score2 = 0
        else:
            sleeptime += 1
    #Left goal - player 2 score
    elif ball_rect.colliderect(goal1_rect):
        goal.play()
        ball_speed[0] = -BALL_SPEED
        ball_rect.center = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
        score2 +=1
        if score2 == MATCH_LENGTH:
            win("Red", RED)
            score1 = score2 = 0
        else:
            sleeptime += 1
    #Ball collision with non-goal sides
    elif ball_rect.colliderect(edge1_rect) or ball_rect.colliderect(edge2_rect):
        ball_speed[0] = -ball_speed[0]
        thunk.play()
    # Paddle collision - reverse speed
    #elif paddle1_rect.colliderect(ball_rect) or paddle2_rect.colliderect(ball_rect):
    #    ball_speed[0] = -ball_speed[0]
    #    boing.play()

    render()

    # Update screen and wait 20 milliseconds
    pygame.display.flip()
    pygame.time.delay(1000*sleeptime)
    pygame.time.delay(20)
