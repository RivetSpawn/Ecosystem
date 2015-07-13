import pygame
import random
import time
import sys
from math import cos, sin, radians

pygame.init() # initialise pygame

# setup colours
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
D_GRAY = (100, 100, 100)
L_GRAY = (200, 200, 200)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
PURPLE = (255, 0, 255)
CYAN = (0, 255, 255)

# setup pygame necessities
screen_size = (500, 500)
screen = pygame.display.set_mode(screen_size)
pygame.display.set_caption('MY GAME')
clock = pygame.time.Clock()
FPS = 30

timer = 0 # initialise timer

# prepare ships list and define population boundaries
ships = []
ship_amount = 1
max_ships = 50


class Object(): # describes the ships/creatures
    max_speed = 4
    max_speed_reverse = -0.2
    def __init__(self, x = int(screen_size[0]/2), y = int(screen_size[1]*0.9)):
        self.x = x
        self.y = y
        self.speed = 0.4
        self.angle = 0
        self.age = 0
        self.colour = GREEN
        self.size = 5
        self.killer = False
        self.killable = False
        self.splittable = False
        self.absorber = False
        self.absorbable = False

    def decide_move(self): # randomly choose an action to change movement speeds/angles
        move_aspect = random.randint(0,3)
        if move_aspect == 0:
            self.speed += random.choice((-0.2, -0.2, -0.4))
        elif move_aspect == 1:
            self.angle -= random.randint(1, 6)
        elif move_aspect == 2:
            self.angle += random.randint(1, 6)
        elif move_aspect == 3:
            self.angle += random.choice((10, -10))
            self.speed += 0.3
        # cleanup angles/speeds
        if self.angle > 360:
            self.angle -= 360
        elif self.angle < 0:
            self.angle += 360
        if self.speed > Object.max_speed:
            self.speed = Object.max_speed
        if self. speed < Object.max_speed_reverse:
            self. speed = Object.max_speed_reverse


    def move(self): # use trig to actually move (in any direction)
        dx = sin(radians(self.angle))
        dy = cos(radians(self.angle))
        self.x += dx * self.speed
        self.y -= dy * self.speed

    def wall_bounce(self): # if an object is out of the screen bounce it back in
        if self.x < 0:
            self.angle *= -1
        elif self.x > screen_size[0]:
            self.angle *= -1
        elif self.y < 0:
            self.angle *= -1
            self.angle += 180
        elif self.y > screen_size[1]:
            self.angle *= -1
            self.angle += 180

    def draw(self): # draw objects to the surface
        pygame.draw.circle(screen, self.colour, (int(self.x), int(self.y)), self.size, 0)

    def age_handle(self): # reconfigure the object based on its age
        if self.age <= 10:
            self.colour = GREEN
            self.killer = False
            self.killable = True
            self.splittable = False
            self.absorber = False
            self.absorbable = False
        elif self.age <=30:
            self.colour = WHITE
            self.killer = False
            self.killable = False
            self.splittable = True
            self.absorber = True
            self.absorbable = False
        elif self.age <=40:
            self.colour = RED
            self.killer = True
            self.killable = False
            self.splittable = False
            self.absorber = False
            self.absorbable = False
            self.speed = 4
        elif self.age <=45:
            self.colour = PURPLE
            self.killer = False
            self.killable = False
            self.splittable = False
            self.absorber = False
            self.absorbable = True
            self.speed = 0.2
        else: # if a ship gets too old remove it, if it's the last one, plant a new one
            if len(ships) == 1:
                ships.append(Object(self.x, self.y))
            ships.remove(self)

    def kill(self): # if the ship's a killer, iterate through the other ships for killables and kill if they touch
        if self.killer:
            for ship in ships:
                if ship.killable:
                    if self.x - self.size <= ship.x and self.x + self.size >= ship.x and self.y - self.size <= ship.y and self.y + self.size >= ship.y:
                        self.size += int(ship.size/4)
                        self.age += 1
                        ships.remove(ship)

    def absorb(self): # if the ship's an absorber, iterate through the other ships for absorbables and absorb if they touch creating 2 new ones
        if self.absorber:
            for ship in ships:
                if ship.absorbable:
                    if ship.x - ship.size <= self.x and ship.x + ship.size >= self.x and ship.y - ship.size <= self.y and ship.y + ship.size >= self.y:
                        self.age = 11
                        ships.remove(ship)
                        ships.append(Object(self.x, self.y))
                        ships.append(Object(self.x, self.y))



    def split(self): # if the ship can split and max ships isn't reached, % chance to create a new one, higher chance with less current ships
        if self.splittable:
            if random.randint(1, 100) <= 10:
                if len(ships) < max_ships:
                    ships.append(Object(self.x, self.y))
            elif len(ships) <= 6:
                if random.randint(1, 100) <= 30:
                    ships.append(Object(self.x, self.y))
            elif len(ships) <= 15:
                if random.randint(1, 100) <= 20:
                    ships.append(Object(self.x, self.y))


for i in range(ship_amount): # initialise starting ships based on ship_amount
    ships.append(Object())

t0 = time.time() # initialise a different kind of clock (the other being pygame clock)

while True: # Main Loop
    t1 = time.time() # check time within loop
    for event in pygame.event.get(): # Event handling
        if event.type == pygame.QUIT:
            pygame.quit(), sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                FPS = 120
            elif event.key == pygame.K_DOWN:
                pass
            elif event.key == pygame.K_LEFT:
                pass
            elif event.key == pygame.K_RIGHT:
                pass
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_UP:
                FPS = 30
            elif event.key == pygame.K_DOWN:
                pass
            elif event.key == pygame.K_LEFT:
                pass
            elif event.key == pygame.K_RIGHT:
                pass

    # Game Logic
    ship_count = len(ships) # count ships
    for ship in ships: # go through every ship
        ship.decide_move()
        ship.move()
        ship.wall_bounce()
        ship.age_handle()
        ship.kill()
        ship.absorb()
        if timer >= 3000: # (pygame clock) if 3 seconds have passed run split(), -1 from ship_count
            ship.split()
            ship_count -= 1
            if ship_count == 0: # if ship_count is 0 (given every ship a chance to split) reset timer
                timer = 0
        if t1-t0 >= 1.0: # 2nd timer to perform events every second, ages ships and increases size
            ship.age += 1
            if ship.colour != PURPLE:
                ship.size += 1
            else:
                ship.size += 3
    if t1-t0 >= 1.0: # if a second did pass, reset the 2nd timer
        t0 = t1



    # Drawing
    screen.fill(BLACK)
    for ship in ships:
        ship.draw()

    # Update Screen
    pygame.display.flip()

    #pygame clock
    milliseconds = clock.tick(FPS)
    timer += milliseconds
