# 1. command to install pygame: pip install pygame
# 2. run it in command prompt
# it should show message : Succesfully installed pygame!

# 3. create a new file with name day7.py
# 4. copy below statements, save your file and run

import pygame

# initializes all the modules
pygame.init()


dim = 500, 500 # screen dimension: width, height
screen = pygame.display.set_mode(dim)
pygame.display.set_caption("My Game") # setting caption/ game title

# circle coordinates
x, y = 200, 250
xstep = 5
ystep = 5
r = 10

# FPS
FPS = 60
clock = pygame.time.Clock()

run = True # variable to store running state of your game

while run:

    # fill the background, parameters: RGB: Red, Green, Blue
    screen.fill((133, 216, 235))

    # setting fps
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        # which key is pressed
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                x -= xstep
                print("LEFT")
            if event.key == pygame.K_RIGHT:
                x += xstep
                print("RIGHT")
            if event.key == pygame.K_UP:
                y -= ystep
                print("UP")
            if event.key == pygame.K_DOWN:
                y += ystep
                print("DOWN")

    # parameter: surface, RGB, centre, radius
    pos = x, y
    # for i in range(4):
    #     pygame.draw.circle(screen, (242, 123, 93), (pos[0]+(i*2*r), pos[1]), r)

    pygame.draw.circle(screen, (242, 123, 93), (pos[0], pos[1]), r)
    pygame.draw.circle(screen, (242, 123, 93), (pos[0]+(2*r), pos[1]), r)
    pygame.draw.circle(screen, (242, 123, 93), (pos[0]+(4*r), pos[1]), r)
    pygame.draw.circle(screen, (242, 123, 93), (pos[0]+(6*r), pos[1]), r)

    # move circle
    
    if x >= dim[0]-r:
        x = dim[0]-r
    if x <= r:
        x = r

    if y >= dim[1]-r:
        y = dim[1]-r
    if y <= r:
        y = r
    
    # if x >= dim[0]-r or x <= r:
        # step *= -1



    pygame.display.update() # update the display
