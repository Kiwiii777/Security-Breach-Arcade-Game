
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
key_items = []
doors = []
key_count = 0

DOOR_INTERACT_DISTANCE = 60
interaction_font = pygame.font.SysFont(None, 28)
key_font = pygame.font.SysFont(None, 32)
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

        self.frames = {
            "up": [pygame.image.load(f"up_{i}.png").convert_alpha() for i in range(1, 4)],
            "right": [pygame.image.load(f"right_{i}.png").convert_alpha() for i in range(1, 4)],
            "down": [pygame.image.load(f"down_{i}.png").convert_alpha() for i in range(1, 4)]
        }
        self.frames["left"] = [pygame.transform.flip(frame, True, False) for frame in self.frames["right"]]
        self.direction = "down"
        self.frame_index = 0
        self.animation_timer = 0
        self.animation_speed = 120
        self.image = self.frames[self.direction][self.frame_index]

    def move(self, keys, walls, bounds):
        dx = int(keys[pygame.K_d] or keys[pygame.K_RIGHT]) - int(keys[pygame.K_a] or keys[pygame.K_LEFT])
        dy = int(keys[pygame.K_s] or keys[pygame.K_DOWN]) - int(keys[pygame.K_w] or keys[pygame.K_UP])
        moving = dx != 0 or dy != 0

        if moving:
            if abs(dx) > abs(dy):
                self.direction = "right" if dx > 0 else "left"
            elif dy != 0:
                self.direction = "down" if dy > 0 else "up"

            direction = pygame.math.Vector2(dx, dy).normalize() * self.speed
        else:
            direction = pygame.math.Vector2(0, 0)

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

        if moving:
            now = pygame.time.get_ticks()
            if now - self.animation_timer >= self.animation_speed:
                self.frame_index = (self.frame_index + 1) % len(self.frames[self.direction])
                self.animation_timer = now
        else:
            self.frame_index = 0
            self.animation_timer = pygame.time.get_ticks()

        self.image = self.frames[self.direction][self.frame_index]

    def reset(self):
        self.pos.update(self.start)
        self.rect.center = self.pos
        self.direction = "down"
        self.frame_index = 0
        self.image = self.frames[self.direction][self.frame_index]

    def draw(self, screen, offset):
        image_rect = self.image.get_rect(midbottom=(self.rect.centerx, self.rect.bottom))
        image_rect.x += offset[0]
        image_rect.y += offset[1]
        screen.blit(self.image, image_rect)


class Enemy: #-a
    def __init__(self, pos, vertical_patrol, min_val, max_val):
        self.pos = pygame.math.Vector2(pos)
        self.start_pos = self.pos.copy()
        self.image_base = pygame.image.load("enemy.png").convert_alpha()
        self.image_base = pygame.transform.rotate(self.image_base, 270)
        self.rect = self.image_base.get_rect(center=self.pos)
        self.collision_rect = pygame.Rect(0, 0, 20, 20)
        self.collision_rect.center = self.pos

        self.vertical_patrol = vertical_patrol
        if vertical_patrol:
            self.base_angle = 90
            self.home_pos = pygame.math.Vector2(self.pos.x, (min_val + max_val)/2)
        else:
            self.base_angle = 0
            self.home_pos = pygame.math.Vector2((min_val + max_val)/2, self.pos.y)

        self.min = min_val
        self.max = max_val
        self.patrol_speed = 5
        self.chase_speed = 16.5
        self.range = 200
        self.vision_angle = 44.4
        self.chase_range = 300
        self.is_patrol = True
        self.is_rotating = False
        self.returning = False
        self.angle = self.base_angle
        self.turn_speed = 5

    def has_line_of_sight(self, target_pos):
        # checks for vision through walls and doors
        start = (round(self.pos.x), round(self.pos.y))
        end = (round(target_pos.x), round(target_pos.y))

        for wall in walls:
            if wall.clipline(start, end):
                return False

        for door in doors:
            if door.rect.clipline(start, end):
                return False

        return True

    def check_player_detection(self, distanceToPlayer, to_player):
        # The dot product checks whether the player is inside the enemy's vision cone.
        cone_limit = cos(radians(self.vision_angle / 2))
        inside_cone = distanceToPlayer <= self.range and self.forward.dot(to_player) >= cone_limit
        if inside_cone and self.has_line_of_sight(player_pos):
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

        cone_limit = cos(radians(self.vision_angle / 2))
        in_vision = (
            distanceToPlayer <= self.range
            and self.forward.dot(to_player) >= cone_limit
            and self.has_line_of_sight(player_pos)
        )
        out_of_chase_range = distance_from_home > self.chase_range

        if not in_vision or out_of_chase_range:
            pursuing.play()
            self.is_patrol = True
            self.returning = True
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

        # Move toward the player with a smaller collision window
        movement = self.forward * self.chase_speed

        next_x = self.pos.x + movement.x
        self.collision_rect.center = (round(next_x), round(self.pos.y))

        if not any(self.collision_rect.colliderect(wall) for wall in walls):
            self.pos.x = next_x

        next_y = self.pos.y + movement.y
        self.collision_rect.center = (round(self.pos.x), round(next_y))

        if not any(self.collision_rect.colliderect(wall) for wall in walls):
            self.pos.y = next_y

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

    def draw_vision(self, screen, offset):
        # draw vision
        center = (
            round(self.pos.x + offset[0]),
            round(self.pos.y + offset[1])
        )

        cone_surface = pygame.Surface(WINDOW_SIZE, pygame.SRCALPHA)
        points = [center]
        half_angle = self.vision_angle / 2

        obstacles = walls + [door.rect for door in doors]

        for angle_offset in range(-int(half_angle), int(half_angle) + 1):
            angle = radians(self.angle + angle_offset)

            direction = pygame.math.Vector2(
                cos(angle),
                -sin(angle)
            )

            end_pos = self.pos + direction * self.range
            start = (round(self.pos.x), round(self.pos.y))
            end = (round(end_pos.x), round(end_pos.y))

            closest_point = end
            closest_distance = self.range

            for obstacle in obstacles:
                intersections = obstacle.clipline(start, end)

                if intersections:
                    hit_pos = pygame.math.Vector2(intersections[0])
                    distance = self.pos.distance_to(hit_pos)

                    if distance < closest_distance:
                        closest_distance = distance
                        closest_point = intersections[0]

            points.append((
                round(closest_point[0] + offset[0]),
                round(closest_point[1] + offset[1])
            ))

        if len(points) >= 3:
            pygame.draw.polygon(
                cone_surface,
                (255, 60, 60, 65),
                points
            )

        screen.blit(cone_surface, (0, 0))

    def draw(self, screen, offset):
        rotated_image = pygame.transform.rotate(self.image_base, self.angle)
        self.rect = rotated_image.get_rect(center=self.pos)
        screen.blit(rotated_image, self.rect.move(offset))

class Keys:
    def __init__(self, pos):
        self.pos = pygame.math.Vector2(pos)
        self.image = pygame.image.load("key.png").convert_alpha()
        self.rect = self.image.get_rect(center=self.pos)

    def draw(self, screen, offset):
        self.rect.center = (round(self.pos.x), round(self.pos.y))
        screen.blit(self.image, self.rect.move(offset))


class Doors:
    def __init__(self, pos):
        self.pos = pygame.math.Vector2(pos)
        self.image = pygame.image.load("door.png").convert_alpha()
        self.rect = self.image.get_rect(center=self.pos)

    def draw(self, screen, offset):
        self.rect.center = (round(self.pos.x), round(self.pos.y))
        screen.blit(self.image, self.rect.move(offset))

running = True
image = pygame.image.load(IMAGE)

enemies = [Enemy((1000, 220), False, 920, 1150), Enemy((350, 450), False, 140, 560), Enemy((820, 580), True, 10, 460)]
player_pos = pygame.math.Vector2(1000, 330)   # stand-in player, map coordinates
map_rect = image.get_rect()

player = Player((1000, 330))
player_pos = player.pos

blackout_until = 0

loose.play()

while running:
    interact_pressed = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN and event.key == pygame.K_e:
            interact_pressed = True

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

    solid_rects = walls + [door.rect for door in doors]
    player.move(pygame.key.get_pressed(), solid_rects, map_rect)

    # collect keys
    for key in key_items[:]:
        if player.rect.colliderect(key.rect):
            key_items.remove(key)
            key_count += 1

    # interact with nearby door
    nearby_door = None
    nearest_distance = DOOR_INTERACT_DISTANCE

    for door in doors:
        distance = player.pos.distance_to(door.pos)

        if distance <= nearest_distance:
            nearby_door = door
            nearest_distance = distance

    # open door
    if interact_pressed and nearby_door is not None:
        if key_count >= 1:
            key_count -= 1
            doors.remove(nearby_door)
            nearby_door = None

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
            blackout_until = pygame.time.get_ticks() + 7500
            break

    offset = (map_position_x, map_position_y)
    screen.blit(image, offset)
    for wall in walls:
        screen_rect = wall.move(map_position_x, map_position_y)
        s = pygame.Surface((wall.width, wall.height), pygame.SRCALPHA)
        s.fill((255, 255, 255, 0))
        screen.blit(s, screen_rect.topleft)
        # outlines for tweaking and troubleshooting if needed so fun!
        # pygame.draw.rect(screen, (255, 255, 255, 0), screen_rect, 2)

    # draw enemy and vision
    for enemy in enemies:
        enemy.draw_vision(screen, offset)
    for enemy in enemies:
        enemy.draw(screen, offset)

    # draw keys
    for key in key_items:
        key.draw(screen, offset)

    # draw doors
    for door in doors:
        door.draw(screen, offset)

    # Display key count
    key_text = key_font.render(f"Keys: {key_count}", True, (255, 255, 255))
    screen.blit(key_text, (20, 20))

    # display door interaction prompt
    if nearby_door is not None:
        if key_count >= 1:
            prompt = "Press E to unlock door"
        else:
            prompt = "You need a key!"

        prompt_surface = interaction_font.render(
            prompt, True, (255, 255, 255)
        )

        prompt_rect = prompt_surface.get_rect(
            center=(
                round(nearby_door.pos.x + map_position_x),
                round(nearby_door.pos.y + map_position_y - 35)
            )
        )

        background_rect = prompt_rect.inflate(16, 10)
        pygame.draw.rect(screen, (30, 30, 30), background_rect, border_radius=6)
        screen.blit(prompt_surface, prompt_rect)

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
    pygame.time.Clock().tick(30)

pygame.quit()
