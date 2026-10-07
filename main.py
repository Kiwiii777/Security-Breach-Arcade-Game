import pygame
from math import *
from random import *

pygame.init()
pygame.display.set_caption("Security Breach")
clock = pygame.time.Clock()

WIDTH = 1280
HEIGHT = 720
screen = pygame.display.set_mode((WIDTH, HEIGHT))

class Walls:
    pass

class Enemy:
    pass

class Keys:
    pass

class Doors:
    pass

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    
    pygame.display.flip()
    clock.tick(60)
    
pygame.quit()