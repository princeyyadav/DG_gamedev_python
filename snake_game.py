import pygame
import random

pygame.init() # initialize all modules

# screen
w, h = 500, 500 # screen dimension
screen = pygame.display.set_mode((w,h))

# caption
pygame.display.set_caption("SNAKE GAME")

# colors
GREEN = (180, 216, 71)
RED = (209, 36, 41)
ORANGE = (228, 107, 41)
WHITE = (255, 255, 255)

# snake body
snake_pos = [[300,300], [320, 300], [340, 300], [360, 300]]
r = 10

step = 20
left = (-step,0)
right = (step,0)
up = (0,-step)
down = (0,step)
direction = left

def draw_snake(snake_pos, screen):
    for pos in snake_pos:
        pygame.draw.circle(screen, RED, pos, r)

# apple
apple_pos = [200,200]

# clock
FPS = 40
clock = pygame.time.Clock()

# Score
score = 0
font = pygame.font.SysFont("Arial", 32, True)

def display_score(score, screen):
    text_surface = font.render("Score: "+str(score), True, WHITE)
    screen.blit(text_surface, (10,10))

timer = 0
run = True
while run:

    screen.fill(GREEN)
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and direction != down:
                direction = up
                print("UP")
            if event.key == pygame.K_DOWN and direction != up:
                print("DOWN")
                direction = down
            if event.key == pygame.K_LEFT and direction != right:
                print("LEFT")
                direction = left
            if event.key == pygame.K_RIGHT and direction != left:
                print("RIGHT")
                direction = right

    # snake movement
    timer += 1 # counter
    if timer%5==0:
        snake_pos = [[snake_pos[0][0]+direction[0], snake_pos[0][1]+direction[1]]] + snake_pos[:-1]
        timer = 0

    # snake eats apple
    if snake_pos[0] == apple_pos:
        apple_pos[0] = (random.randint(20, w-10)//20)*20 # x coord
        apple_pos[1] = (random.randint(20, h-10)//20)*20 # y coord
        snake_pos.append(snake_pos[-1]) # increse snake's length
        score += 1
        print(score)

    # game over
    for pos in snake_pos[1:]:
        if snake_pos[0] == pos:
            run = False
            print("Game Over")


    # draw snake
    draw_snake(snake_pos, screen)

    # draw apple
    pygame.draw.circle(screen, ORANGE, apple_pos, r)

    # display score
    display_score(score, screen)

    pygame.display.update()

