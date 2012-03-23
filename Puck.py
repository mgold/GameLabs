import pygame
from pygame.constants import *

def abs (x):
    if x < 0:
        return -x
    return x

class Puck(pygame.sprite.Sprite):
    def __init__(self, screen, x0, y0):
        self.radius = 30
        self.area = self.radius**2
        self.screen = screen

        self.dy = self.dx = self.maxSpeed = 10
        self.x = self.x0 = x0
        self.y = self.y0 = y0

        self.timer = 0

    def reset(self):
        self.dy = self.dx = self.maxSpeed
        if self.x < self.x0:
            self.dx *= -1
            self.dy *= -1
        self.x = self.x0
        self.y = self.y0
        self.timer = 0
        self.rectify()

    def rectify(self):
        self.rect = pygame.Rect(self.x - self.radius,
                                self.y - self.radius,
                                self.radius, self.radius)

    def collidex(self):
        self.dx *= -1

    def collidey(self):
        self.dy *= -1

    def update(self):
        self.dx *= .999
        self.dy *= .999
        if abs(self.dx) and abs(self.dy) < 0.005:
            self.timer += 1
        else:
            self.timer = 0
        if self.timer >= 50:
            self.reset()
        else:
            self.x += self.dx
            self.y += self.dy
            self.rectify()

    def draw(self):
       pygame.draw.circle(self.screen, (0,0,0), (int(self.x), int(self.y)), self.radius)
