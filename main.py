import pygame
from math import *
from random import *

pygame.init()
pygame.display.set_caption("Security Breach")

IMAGE = "map.png"
WINDOW_SIZE = (800,600)
WINDOW_TITLE = "Pygame Image"
map_position_x = -480
map_position_y = -95
rect_pos_x = 100
rect_pos_y = 100
OUTPUT_FILE = "walls.txt"
font = pygame.font.SysFont(None, 48)
blackout_text = ""

pursuing = pygame.mixer.Sound("pursuing.mp3")
pursuing.set_volume(0.5)
loose = pygame.mixer.Sound("loose.mp3")
loose.set_volume(0.5)
found = pygame.mixer.Sound("found.mp3")
found.set_volume(0.5)
lose = pygame.mixer.Sound("lose.mp3")
lose.set_volume(0.5)
win = pygame.mixer.Sound("win.mp3")
win.set_volume(0.5)

pygame.mixer.music.load("background.mp3")
pygame.mixer.music.set_volume(0.2)
pygame.mixer.music.play(-1)

screen = pygame.display.set_mode(WINDOW_SIZE)

incremented_x = 0
incremented_y = 0
incremented = (incremented_x, incremented_y)

points = []  # Stores up to two (x, y) tuples: [p1, p2]
line_stats = None  # Stores calculated stats: (length, midpoint)

walls = [
    pygame.Rect(1188, 486, 20, 200),
    pygame.Rect(1030, 489, 169, 20),
    pygame.Rect(1036, 392, 171, 20),
    pygame.Rect(1190, 90, 20, 309),
    pygame.Rect(1188, -15, 20, 109),
    pygame.Rect(1096, -2, 20, 189),
    pygame.Rect(869, 262, 242, 20),
    pygame.Rect(869, -14, 20, 422),
    pygame.Rect(879, 388, 74, 20),
    pygame.Rect(773, -38, 20, 190),
    pygame.Rect(518, 136, 174, 20),
    pygame.Rect(615, -18, 20, 161),
    pygame.Rect(1029, 587, 20, 115), 
    pygame.Rect(455, 675, 822, 20), 
    pygame.Rect(869, 486, 20, 201), 
    pygame.Rect(745, 486, 203, 20), 
    pygame.Rect(774, 231, 20, 265), 
    pygame.Rect(613, 233, 171, 20), 
    pygame.Rect(616, 242, 20, 70), 
    pygame.Rect(631, 242, 20, 71), 
    pygame.Rect(646, 241, 20, 72), 
    pygame.Rect(647, 293, 49, 20), 
    pygame.Rect(475, 390, 218, 20), 
    pygame.Rect(517, 149, 20, 254), 
    pygame.Rect(583, 399, 20, 139), 
    pygame.Rect(593, 519, 40, 20), 
    pygame.Rect(615, 489, 20, 40), 
    pygame.Rect(588, 485, 73, 20), 
    pygame.Rect(599, 498, 20, 33), 
    pygame.Rect(486, 520, 102, 20), 
    pygame.Rect(489, 484, 20, 45),
    pygame.Rect(489, 615, 147, 20),
    pygame.Rect(614, 623, 20, 64),
    pygame.Rect(359, 388, 125, 20),
    pygame.Rect(455, 232, 20, 166),
    pygame.Rect(455, -33, 20, 188),
    pygame.Rect(359, -20, 20, 142),
    pygame.Rect(357, 203, 20, 203),
    pygame.Rect(262, -21, 20, 430),
    pygame.Rect(232, 134, 41, 20),
    pygame.Rect(-5, 136, 158, 20),
    pygame.Rect(101, 102, 20, 116),
    pygame.Rect(99, -11, 20, 39),
    pygame.Rect(101, 297, 20, 402),
    pygame.Rect(-35, 678, 491, 20),
    pygame.Rect(293, 616, 20, 72),
    pygame.Rect(302, 615, 108, 20),
    pygame.Rect(389, 487, 20, 135),
    pygame.Rect(263, 486, 138, 20),
    pygame.Rect(262, 497, 20, 42),
    pygame.Rect(231, 519, 42, 20),
    pygame.Rect(111, 519, 42, 20),
    pygame.Rect(112, 614, 107, 20),
    pygame.Rect(199, 392, 20, 50),
    pygame.Rect(206, 391, 73, 20)
]           # Stores finalized pygame.Rect objects
drawing = False      # Tracks if mouse is currently held down
start_pos = None     # (x, y) where drag started
current_pos = None   # Current mouse position during drag

def screen_to_map(pos):
    return (pos[0] - map_position_x, pos[1] - map_position_y)

def get_normalized_rect(p1, p2):
    """Generates a pygame.Rect with a fixed width or height of 20px based on drag direction."""
    WALL_THICKNESS = 20

    dx = p2[0] - p1[0]
    dy = p2[1] - p1[1]

    # If horizontal drag is larger, lock height to 20
    if abs(dx) >= abs(dy):
        x = min(p1[0], p2[0])
        y = p1[1] - (WALL_THICKNESS // 2)  # Centers the 20px thickness on the mouse Y line
        w = max(abs(dx), 1)
        h = WALL_THICKNESS
    # If vertical drag is larger, lock width to 20
    else:
        x = p1[0] - (WALL_THICKNESS // 2)  # Centers the 20px thickness on the mouse X line
        y = min(p1[1], p2[1])
        w = WALL_THICKNESS
        h = max(abs(dy), 1)

    return pygame.Rect(x, y, w, h)

class Walls:
    pass

class Player:
    def __init__(self, pos):
        self.pos = pygame.math.Vector2(pos)
        self.start = pygame.math.Vector2(pos)
        self.speed = 15
        self.size = 20
        self.rect = pygame.Rect(0, 0, self.size, self.size)
        self.rect.center = self.pos

        self.image = pygame.image.load("player.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (40, 40))

    def move(self, keys, walls, bounds):
        dx = (keys[pygame.K_d] or keys[pygame.K_RIGHT]) - (keys[pygame.K_a] or keys[pygame.K_LEFT])
        dy = (keys[pygame.K_s] or keys[pygame.K_DOWN]) - (keys[pygame.K_w] or keys[pygame.K_UP])
        direction = pygame.math.Vector2(dx, dy)
        if direction.length() > 0:
            direction = direction.normalize() * self.speed
        self.pos.x += direction.x
        self.rect.centerx = round(self.pos.x)
        for wall in walls:
            if self.rect.colliderect(wall):
                if direction.x > 0:
                    self.rect.right = wall.left
                elif direction.x < 0:
                    self.rect.left = wall.right
                self.pos.x = self.rect.centerx
        self.pos.y += direction.y
        self.rect.centery = round(self.pos.y)
        for wall in walls:
            if self.rect.colliderect(wall):
                if direction.y > 0:
                    self.rect.bottom = wall.top
                elif direction.y < 0:
                    self.rect.top = wall.bottom
                self.pos.y = self.rect.centery
        self.rect.clamp_ip(bounds)
        self.pos.update(self.rect.center)

    def reset(self):
        self.pos.update(self.start)
        self.rect.center = self.pos

    def draw(self, screen, offset):
        image_rect = self.image.get_rect(center=self.rect.center)
        screen.blit(self.image, image_rect.move(offset))

class Enemy: #-a
    def __init__(self, pos, vertical_patrol, min_val, max_val):
        self.pos = pygame.math.Vector2(pos)
        self.start_pos = self.pos.copy()
        self.image_base =pygame.image.load("enemy.png").convert_alpha()
        self.image_base = pygame.transform.rotate(self.image_base, 270)
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
        self.range = 200
        self.chase_range = 300
        self.is_patrol = True
        self.is_rotating = False
        self.returning = False
        self.angle = self.base_angle
        self.turn_speed = 5
        self.cooldown = 30

    def check_player_detection(self, distanceToPlayer, to_player):
        if distanceToPlayer <= self.range and self.forward.dot(to_player) > 0.7:
            if self.is_patrol or self.returning or self.is_rotating:
                self.is_patrol = False
                self.returning = False
                self.is_rotating = False
                found.play()
                return True
        return False
        
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
        
        # Check player detection in all non-chase states (patrol, return_home, rotate)
        if self.is_patrol:
            if self.check_player_detection(distanceToPlayer, to_player):
                self.chase(distanceToPlayer, to_player)
                return

        # actions
        if self.returning:
            self.return_home()
            return
        if not self.is_rotating:
            if self.is_patrol:
                self.patrol()
            else:
                self.chase(distanceToPlayer, to_player)
        else:
            self.rotate()
        
    def patrol(self):
        # Move forward
        self.pos += self.patrol_speed * self.forward
        
        if self.vertical_patrol:
            # snap back upper bound
            if self.pos.y > self.max:
                self.pos.y = self.max
                self.turn_around()
            # snap back lower bound
            elif self.pos.y < self.min:
                self.pos.y = self.min
                self.turn_around()
        else:
            # same but horiz
            if self.pos.x > self.max:
                self.pos.x = self.max
                self.turn_around()
            # same but horiz
            elif self.pos.x < self.min:
                self.pos.x = self.min
                self.turn_around()
    
    def chase(self, distanceToPlayer, to_player):
        distance_from_home = self.pos.distance_to(self.home_pos)
        
        in_vision = (distanceToPlayer <= self.range) and (self.forward.dot(to_player) > 0.7)
        out_of_chase_range = distance_from_home > self.chase_range
        
        if distanceToPlayer <= 30 and self.cooldown <= 0:
            self.shoot()
            lose.play()
        
        if not in_vision or out_of_chase_range:
            pursuing.play()
            self.is_patrol = True
            self.returning = True
            self.cooldown = 30
            return

        # cross to rotate towards player
        cross = self.forward.cross(to_player)
        
        if cross > 0:
            self.angle -= self.turn_speed
        elif cross < 0:
            self.angle += self.turn_speed

        self.angle %= 360

        # update forward
        self.forward = pygame.math.Vector2(
            cos(radians(self.angle)),
            -sin(radians(self.angle))
        )

        self.pos += self.forward * self.chase_speed 
        
        self.cooldown -= 1 

    def turn_around(self):
        self.target_angle = (self.angle + 180) % 360
        self.is_rotating = True
    
    def rotate(self):
        diff = (self.target_angle - self.angle + 180) % 360 - 180
        if abs(diff) <= self.turn_speed:
            self.angle = self.target_angle
            self.returning = False
            self.is_patrol = True
            self.is_rotating = False
        else:
            self.angle += self.turn_speed if diff > 0 else -self.turn_speed
        self.angle %= 360
    
    def return_home(self):
        direction = self.home_pos - self.pos
        distance = direction.length()
        arrival_threshold = self.patrol_speed

        if distance > arrival_threshold:
            to_home = direction.normalize()
            cross = self.forward.cross(to_home)

            if cross > 0:
                self.angle -= self.turn_speed
            elif cross < 0:
                self.angle += self.turn_speed

            self.angle %= 360

            self.forward = pygame.math.Vector2(
                cos(radians(self.angle)),
                -sin(radians(self.angle))
            )

            self.pos += self.forward * self.patrol_speed
        else:
            self.pos = self.home_pos.copy()
            self.returning = False
            self.target_angle = self.base_angle
            self.is_rotating = True
            
    def shoot(self):
        net.append(Net(self.pos, self.forward))
        self.cooldown = 30

    def draw(self, screen, offset):
        rotated_image = pygame.transform.rotate(self.image_base, self.angle)
        self.rect = rotated_image.get_rect(center=self.pos)
        screen.blit(rotated_image, self.rect.move(offset))

class Net:
    def __init__(self, pos, forward):
        self.pos = pygame.math.Vector2(pos)
        self.forward = forward
        self.speed = 23
        self.image = pygame.image.load("net.png").convert_alpha()
        self.rect = self.image.get_rect(center=self.pos)
    
    def move(self):
        self.pos += self.speed * self.forward
        self.rect.center = self.pos
        
    def draw(self, screen, offset):
        self.rect.center = self.pos
        screen.blit(self.image, self.rect.move(offset))
        
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
image = pygame.image.load(IMAGE)

enemies = [Enemy((1000, 220), False, 920, 1150), Enemy((350, 450), False, 140, 560), Enemy((820, 580), True, 10, 460)]
net = []
player_pos = pygame.math.Vector2(1000, 330)   # stand-in player, map coordinates
map_rect = image.get_rect()

player = Player((1000, 330))
player_pos = player.pos

blackout_until = 0

loose.play()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
    keys = pygame.key.get_pressed()    
    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
        map_position_x -= 10
    elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        map_position_x += 10
    elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
        map_position_y += 10
    elif keys[pygame.K_UP] or keys[pygame.K_w]:
        map_position_y -= 10

    map_position_x = max(-480, min(0, map_position_x))
    map_position_y = max(-100, min(5, map_position_y))

    player.move(pygame.key.get_pressed(), walls, map_rect)

    map_position_x = max(-480, min(0, WINDOW_SIZE[0] // 2 - int(player.pos.x)))
    map_position_y = max(-100, min(5, WINDOW_SIZE[1] // 2 - int(player.pos.y)))

    screen.blit(image, (map_position_x, map_position_y))
    for enemy in enemies:
        enemy.act()
        if enemy.pos.distance_to(player.pos) < 25:
            player.reset()
            for e in enemies:
                e.reset()
                lose.play()
            net.clear()
            blackout_until = pygame.time.get_ticks() + 7500
            break
    for n in net[:]:
        n.move()
        if n.rect.collidepoint(player_pos.x, player_pos.y):
            net.remove(n)
        elif not map_rect.collidepoint(n.pos.x, n.pos.y) or any(n.rect.colliderect(w) for w in walls):
            net.remove(n)

    offset = (map_position_x, map_position_y)
    screen.blit(image, offset)
    for wall in walls:
        screen_rect = wall.move(map_position_x, map_position_y)
        s = pygame.Surface((wall.width, wall.height), pygame.SRCALPHA)
        s.fill((255, 255, 255, 0))
        screen.blit(s, screen_rect.topleft)
        # outlines for tweaking and troubleshooting if needed so fun!
        # pygame.draw.rect(screen, (255, 255, 255, 0), screen_rect, 2)
    
    for enemy in enemies:
        enemy.draw(screen, offset)
    for n in net:
        n.draw(screen, offset)
    player.draw(screen, offset)
    print(player_pos)
    if pygame.time.get_ticks() < blackout_until:
        screen.fill((0, 0, 0))
        text = font.render(blackout_text, True, (255, 255, 255))
        screen.blit(text, text.get_rect(center=(WINDOW_SIZE[0] // 2, WINDOW_SIZE[1] // 2)))
        pygame.display.flip()
        pygame.time.Clock().tick(60)
        continue
    if (player_pos.x <= 103 and player_pos.y <= 100):
        blackout_text = "You won!"
        blackout_until = pygame.time.get_ticks() + 7500
        win.play()
        player.reset()
            
    pygame.display.flip()
    pygame.time.Clock().tick(60)
    
pygame.quit()