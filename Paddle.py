import pygame
from pygame.constants import *

def bound (lo, val, hi):
    return max(lo, min(val, hi))

class Paddle(pygame.sprite.Sprite):
    def __init__(self, screen, minx, maxx, color):
        self.radius = 50
        self.screen = screen
        self.color = color
        self.minx = minx + self.radius
        self.maxx = maxx - self.radius
        self.miny = 0
        self.maxy = screen.get_height() - self.radius

        self.x = (self.minx + self.maxx)//2
        self.y = (self.miny + self.maxy)//2
        self.moveSpeed = 10

    def update(self, commands):
        if K_w in commands or K_UP in commands:
            self.y -= self.moveSpeed
        if K_s in commands or K_DOWN in commands:
            self.y += self.moveSpeed
        if K_a in commands or K_LEFT in commands:
            self.x -= self.moveSpeed
        if K_d in commands or K_RIGHT in commands:
            self.x += self.moveSpeed
        self.x = bound (self.minx, self.x, self.maxx)
        self.y = bound (self.miny, self.y, self.maxy)

    def draw(self):
       pygame.draw.circle(self.screen, self.color, (self.x, self.y),self.radius)

