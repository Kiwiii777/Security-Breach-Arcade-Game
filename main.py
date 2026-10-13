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
    def __init__(self, pos, vertical_patrol, min_val, max_val):
        self.pos = pygame.math.Vector2(pos)
        self.image_base = pygame.image.load("enemy.png").convert_alpha()
        self.rect = self.image_base.get_rect(center=self.pos)
        
        self.vertical_patrol = vertical_patrol
        if vertical_patrol:
            self.base_angle = 90
            self.home_pos = pygame.math.Vector2(self.pos.x, (min_val + max_val)/2)
        else:
            self.base_angle = 0
            self.home_pos = pygame.math.Vector2((min_val + max_val)/2, self.pos.y)
                    
        self.min = min_val
        self.max = max_val
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
        self.forward = pygame.math.Vector2(
            cos(radians(self.angle)),
            -sin(radians(self.angle))
        )
        
        distanceToPlayer = self.pos.distance_to(player_pos)
        
        if distanceToPlayer > 0:
            to_player = (player_pos - self.pos).normalize()
        else:
            to_player = pygame.math.Vector2(0, 0)
        
        # actions
        if self.returning:
            self.return_home()
            return
        if not self.is_rotating:
            if self.is_patrol:
                self.patrol(distanceToPlayer, to_player)
            else:
                self.chase(distanceToPlayer, to_player)
        else:
            self.rotate()
        
    def patrol(self, distanceToPlayer, to_player):
        if distanceToPlayer <= self.range and self.forward.dot(to_player) > 0.7:
            self.is_patrol = False
            return
        else:
            # Move forward
            self.pos += self.patrol_speed * self.forward
            
            if self.vertical_patrol:
                # snap back upper bound
                if self.pos.y > self.max:
                    self.pos.y = self.max
                    self.is_rotating = True
                # snap back lower bound
                elif self.pos.y < self.min:
                    self.pos.y = self.min
                    self.is_rotating = True
            else:
                # same but horiz
                if self.pos.x > self.max:
                    self.pos.x = self.max
                    self.is_rotating = True
                # same but horiz
                elif self.pos.x < self.min:
                    self.pos.x = self.min
                    self.is_rotating = True
    
    def chase(self, distanceToPlayer, to_player):
        distance_from_home = self.pos.distance_to(self.home_pos)
        
        in_vision = (distanceToPlayer <= self.range) and (self.forward.dot(to_player) > 0.7)
        out_of_chase_range = distance_from_home > self.chase_range
        
        if distanceToPlayer <= 30 and self.cooldown <= 0:
            self.shoot()
        
        if not in_vision or out_of_chase_range:
            self.is_patrol = True
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
        self.forward = pygame.math.Vector2(
            cos(radians(self.angle)),
            -sin(radians(self.angle))
        )

        self.pos += self.forward * self.chase_speed 
        
        self.cooldown -= 1 
    
    def rotate(self):
        if self.angle != self.base_angle:
            self.angle += self.turn_speed
        else:
            self.returning = False
            self.is_patrol = True
            self.is_rotating = False
    
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

            self.forward = pygame.math.Vector2(
                cos(radians(self.angle)),
                -sin(radians(self.angle))
            )

            self.pos += to_home * self.patrol_speed
        else:
            self.returning = False
            self.is_rotating = True
            
    def shoot(self):
        net.append(Net(self.pos, self.forward))
        self.cooldown = 30

    def draw(self, screen):
        rotated_image = pygame.transform.rotate(self.image_base, self.angle)
        self.rect = rotated_image.get_rect(center=self.pos)
        screen.blit(rotated_image, self.rect)

class Net:
    def __init__(self, pos, forward):
        self.pos = pygame.math.Vector2(pos)
        self.forward = forward
        self.speed = 23
        self.image = pygame.image.load("net.png").convert_alpha()
        self.rect = self.image.get_rect(center=self.pos)
    
    def move(self):
        self.pos += self.speed * self.forward
        
    def draw(self, screen):
        self.rect.center = self.pos
        screen.blit(self.image, self.rect)
        
class Keys:
    def __init__(self, pos):
        self.pos = pygame.math.Vector2(pos)
        self.image = pygame.image.load("key.png").convert_alpha()
        self.rect = self.image.get_rect(center=self.pos)

    def draw(self, screen):
        self.rect.center = self.pos
        screen.blit(self.image, self.rect)

class Doors:
    def __init__(self, pos):
        self.pos = pygame.math.Vector2(pos)
        self.image = pygame.image.load("door.png").convert_alpha()
        self.rect = self.image.get_rect(center=self.pos)

    def draw(self, screen):
        self.rect.center = self.pos
        screen.blit(self.image, self.rect)

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    pygame.display.flip()
    clock.tick(60)
    
pygame.quit()
