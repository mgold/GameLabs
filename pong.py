import pygame, sys

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
PADDLE1_START_X = 10
PADDLE1_START_Y = 20
PADDLE2_START_X = 780
PADDLE2_START_Y = 20
PADDLE_WIDTH = 10
PADDLE_HEIGHT = 100
BALL_SPEED = 10
BALL_WIDTH_HEIGHT = 16
MATCH_LENGTH = 11

def render():
    # Clear screen
    screen.fill((255, 255, 255))
    pygame.draw.rect(screen, (0, 0, 255), centerline1_rect)
    pygame.draw.rect(screen, (255, 0, 0), centerline2_rect)

    # Render the ball and paddles
    pygame.draw.rect(screen, (0, 0, 255), paddle1_rect) # Your paddle
    pygame.draw.rect(screen, (255, 0, 0), paddle2_rect) # Opponent paddle
    pygame.draw.circle(screen, (0, 0, 0), ball_rect.center, ball_rect.width / 2) # The ball

    # Render the scores
    score1_text = font.render(str(score1), True, (0, 0, 255))
    screen.blit(score1_text, ((SCREEN_WIDTH / 4) - font.size(str(score1))[0] / 2, 5)) # The score1
    score2_text = font.render(str(score2), True, (255, 0, 0))
    screen.blit(score2_text, ((SCREEN_WIDTH * 3 / 4) - font.size(str(score2))[0] / 2, 5)) # The score2


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

boing = pygame.mixer.Sound("boing.wav")

# This is a rect that contains the ball at the beginning it is set in the center of the screen
ball_rect = pygame.Rect((SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2), (BALL_WIDTH_HEIGHT, BALL_WIDTH_HEIGHT))

# Speed of the ball (x, y)
ball_speed = [BALL_SPEED, BALL_SPEED]

# Paddles are  vertically centered on the respective sides
paddle1_rect = pygame.Rect((PADDLE1_START_X, PADDLE1_START_Y), (PADDLE_WIDTH, PADDLE_HEIGHT))
paddle2_rect = pygame.Rect((PADDLE2_START_X, PADDLE2_START_Y), (PADDLE_WIDTH, PADDLE_HEIGHT))

centerline1_rect = pygame.Rect((SCREEN_WIDTH/2 -2, 0), (3, SCREEN_HEIGHT))
centerline2_rect = pygame.Rect((SCREEN_WIDTH/2 +1, 0), (3, SCREEN_HEIGHT))

# Scoring: 1 point if you hit the ball, -5 point if you miss the ball
score1 = 0
score2 = 0

# Load the font for displaying the score and game result
font = pygame.font.Font(None, 30)
winFont = pygame.font.Font(None, 72)

# Game loop
while True:
    sleeptime = 0
    
    # Event handler
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit(0)
            pygame.quit()
        # Control the paddle with the mouse
        elif event.type == pygame.MOUSEMOTION:
            paddle1_rect.centery = event.pos[1]
            # correct paddle position if it's going out of window
            if paddle1_rect.top < 0:
                paddle1_rect.top = 0
            elif paddle1_rect.bottom >= SCREEN_HEIGHT:
                paddle1_rect.bottom = SCREEN_HEIGHT

            if paddle2_rect.top < 0:
                paddle2_rect.top = 0
            elif paddle2_rect.bottom >= SCREEN_HEIGHT:
                paddle2_rect.bottom = SCREEN_HEIGHT

    # This test if up or down keys are pressed; if yes, move the paddle
    if pygame.key.get_pressed()[pygame.K_UP] and paddle1_rect.top > 0:
        paddle1_rect.top -= BALL_SPEED
    elif pygame.key.get_pressed()[pygame.K_DOWN] and paddle1_rect.bottom < SCREEN_HEIGHT:
        paddle1_rect.top += BALL_SPEED
    elif pygame.key.get_pressed()[pygame.K_ESCAPE]:
        pygame.quit()

    # Update ball position
    ball_rect.left += ball_speed[0]
    ball_rect.top += ball_speed[1]

    #Paddle AI
    paddle2_rect.centery = ball_rect.centery

    # Ball collision with rails
    if ball_rect.top <= 0 or ball_rect.bottom >= SCREEN_HEIGHT:
        ball_speed[1] = -ball_speed[1]
    if ball_rect.right >= SCREEN_WIDTH: #Right rail - player 1 score
        ball_speed[0] = BALL_SPEED
        ball_rect = pygame.Rect((SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2), (BALL_WIDTH_HEIGHT, BALL_WIDTH_HEIGHT))
        score1 += 1
        if score1 == MATCH_LENGTH:
            win("Blue", (0, 0, 255))
            score1 = score2 = 0
        else:
            sleeptime += 1
    if ball_rect.left <= 0: #Left rail - player 2 score
        ball_speed[0] = -BALL_SPEED
        #ball_rect = pygame.Rect((SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2), (BALL_WIDTH_HEIGHT, BALL_WIDTH_HEIGHT))
        ball_rect.center = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
        score2 +=1
        if score2 == MATCH_LENGTH:
            win("Red", (255, 0, 0))
            score1 = score2 = 0
        else:
            sleeptime += 1

    # Test if the ball is hit by the paddle; if yes reverse speed
    if paddle1_rect.colliderect(ball_rect):
        ball_speed[0] = -ball_speed[0]
        boing.play()

    if paddle2_rect.colliderect(ball_rect):
        ball_speed[0] = -ball_speed[0]
        boing.play()

    render()

    # Update screen and wait 20 milliseconds
    pygame.display.flip()
    pygame.time.delay(1000*sleeptime)
    pygame.time.delay(20)
