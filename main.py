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
    def __init__(self, pos, vertical_patrol, min, max):
        self.pos = pos
        if vertical_patrol:
            self.angle = 90
            self.home_pos = pygame.math.Vector2(pos.x, (min + max)/2)
        else:
            self.angle = 0
            self.home_pos = pygame.math.Vector2((min + max)/2, pos.y)
                    
        self.min = min
        self.max = max
        self.patrol_speed = 10
        self.chase_speed = 15
        self.range = 100
        self.chase_range = 300
        
        
    def act(self):
        self.forward = pygame.Math.Vector2(
            cos(radians(self.angle)),
            -sin(radians(self.angle))
        )
        
        distanceToPlayer = self.pos.distance_to(player_pos)
        
        if distanceToPlayer <= self.range and 
        

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