import pygame
from pygame.constants import *

def bound (lo, val, hi):
    return max(lo, min(val, hi))

class Paddle(pygame.sprite.Sprite):
    def __init__(self, screen, minx, maxx, color):
        self.radius = 50
        self.area = self.radius**2
        self.screen = screen
        self.color = color
        self.minx = minx + self.radius
        self.maxx = maxx - self.radius
        self.miny = 0
        self.maxy = screen.get_height() - self.radius

        self.x = (self.minx + self.maxx)//2
        self.y = (self.miny + self.maxy)//2
        self.dx = self.dy = 0
        self.moveSpeed = 15

    def update(self, commands):
        self.dx = self.dy = 0 
        if K_w in commands or K_UP in commands:
            self.dy -= self.moveSpeed
        if K_s in commands or K_DOWN in commands:
            self.dy += self.moveSpeed
        if K_a in commands or K_LEFT in commands:
            self.dx -= self.moveSpeed
        if K_d in commands or K_RIGHT in commands:
            self.dx += self.moveSpeed
        self.x += self.dx
        self.y += self.dy
        self.x = bound (self.minx, self.x, self.maxx)
        self.y = bound (self.miny, self.y, self.maxy)
        self.rect = pygame.Rect(self.x - self.radius,                               
                                self.y - self.radius,                               
                                self.radius, self.radius)

    def draw(self):
       pygame.draw.circle(self.screen, self.color, (self.x, self.y),self.radius)

