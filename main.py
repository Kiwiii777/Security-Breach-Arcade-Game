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

class Enemy: # -a
    def __init__(self, pos, vertical_patrol, min, max):
        self.pos = pos
        if vertical_patrol:
            self.base_angle = 90
            self.home_pos = pygame.math.Vector2(pos.x, (min + max)/2)
        else:
            self.base_angle = 0
            self.home_pos = pygame.math.Vector2((min + max)/2, pos.y)
                    
        self.min = min
        self.max = max
        self.patrol_speed = 10
        self.chase_speed = 15
        self.range = 100
        self.chase_range = 300
        self.is_patrol = True
        self.is_rotating = False
        self.returning = False
        self.angle = self.base_angle
        self.turn_speed = 5
        self.cooldown = 30
        
    def act(self):
        self.forward = pygame.Math.Vector2(
            cos(radians(self.angle)),
            -sin(radians(self.angle))
        )
        
        distanceToPlayer = self.pos.distance_to(player_pos)
        to_player = (player_pos - self.pos).normalize()
        
        # actions
        if self.returning:
            self.return_home()
            return
        if not self.rotating:
            if self.is_patrol:
                self.patrol(distanceToPlayer, to_player)
            else:
                self.chase()
        else:
            self.rotate()
        
    def patrol(self, distanceToPlayer, to_player):
        if distanceToPlayer <= self.range and self.forward.dot(to_player) > 0.7:
            patrol = False
            return
        else:
            # Move forward
            self.pos += self.patrol_speed * self.forward
            
            if self.vertical_patrol:
                # snap back upper bound
                if self.pos.y > self.max:
                    self.pos.y = self.max
                    self.rotating = True
                # snap back lower bound
                elif self.pos.y < self.min:
                    self.pos.y = self.min
                    self.rotating = True
            else:
                # same but horiz
                if self.pos.x > self.max:
                    self.pos.x = self.max
                    self.rotating = True
                # same but horiz
                elif self.pos.x < self.min:
                    self.pos.x = self.min
                    self.rotating = True
    
    def chase(self, distanceToPlayer, to_player):
        distance_from_home = self.pos.distance_to(self.home_pos)
        
        in_vision = (distanceToPlayer <= self.range) and (self.forward.dot(to_player) > 0.7)
        out_of_chase_range = distance_from_home > self.chase_range
        
        if distanceToPlayer <= 30 and self.cooldown >= 0:
            self.shoot()
        
        if not in_vision or out_of_chase_range:
            self.chasing = False
            self.returning = True
            self.cooldown = 30
            return

        # cross to rotate towards player
        cross = self.forward.cross(to_player)
        
        if cross > 0:
            self.angle += self.turn_speed
        elif cross < 0:
            self.angle -= self.turn_speed

        # update forward
        self.forward = pygame.Math.Vector2(
            cos(radians(self.angle)),
            -sin(radians(self.angle))
        )

        self.pos += self.forward * self.chase_speed 
        
        self.cooldown -= 1 
    
    def rotating(self):
        if self.angle != self.base_angle:
            self.angle += self.turn_speed
        else:
            self.is_returning = False
            self.is_patrol = True
    
    def return_home(self):
        direction = self.home_pos - self.pos
        distance = direction.length()
        arrival_threshold = 2.0

        if distance > arrival_threshold:
            to_home = direction.normalize()
            cross = self.forward.cross(to_home)

            if cross > 0:
                self.angle += self.turn_speed
            elif cross < 0:
                self.angle -= self.turn_speed

            self.forward = pygame.Math.Vector2(
                cos(radians(self.angle)),
                -sin(radians(self.angle))
            )

            self.pos += to_home * self.patrol_speed
        
        else:
            self.returning = False
            self.is_rotating = True
            
    def shoot(self):
        net.append(Net(self.pos, self.forward))

class Net:
    def __init__(self, pos, forward):
        self.pos = pos
        self.forward = forward
        self.speed = 23
    
    def move(self):
        self.pos += self.speed * self.forward
        
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