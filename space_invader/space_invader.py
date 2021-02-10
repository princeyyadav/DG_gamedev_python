import pygame
import random

pygame.init()

w, h = 800, 600
screen = pygame.display.set_mode((w,h))
pygame.display.set_caption("SPACE INVADER")
# icon
icon = pygame.image.load("assets/ufo.png")
pygame.display.set_icon(icon)

FPS = 60
clock = pygame.time.Clock()

class Player:

    def __init__(self):
        self.image = pygame.image.load("assets/spaceship.png")
        self.x = 400
        self.y = 450
        self.xvel = 0

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))

    def move(self):
        self.x += self.xvel

        if self.x <= 0:
            self.x = 0
        elif self.x >= 736: # 800-64, screen_width - image_width
            self.x = 736

class Bullet:

    def __init__(self, px):
        self.image = pygame.image.load("assets/bullet.png")
        self.x = px+16 # player_x + constant
        self.y = 470
        self.xvel = 0
        self.yvel = 10
        self.state = "ready"

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))

    def move(self, px):
        if self.state == "ready":
            self.x = px+16

        if self.state == "fired":
            self.y -= self.yvel

            if self.y <= 0:
                self.x = px+16
                self.y = 470
                self.state = "ready"


    def respawn(self, px):
        self.x = px+16
        self.y = 470
        self.state = "ready"


    def collide(self, e):
        distance = ((self.x-e.x)**2 + (self.y-e.y)**2)**(0.5)
        if distance <= 30:
            return True
        else:
            return False

    

class Enemy:

    def __init__(self):
        self.image = pygame.image.load("assets/alien.png")
        self.x = 200
        self.y = 150
        self.xvel = 7
        self.yvel = 50

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))

    def move(self):
        self.x += self.xvel

        if self.x <= 0 or self.x>=800-64:
            self.xvel *= -1 # reverse the vel
            self.y += self.yvel # move the enemy down

    
    def respawn(self): # reappear/ reposition at a random place
        self.x = random.randint(0, 736)
        self.y = random.randint(50, 300)


class Text:

    def __init__(self, text, size, pos, color=(255,255,255)):
        self.font = pygame.font.SysFont("Arial", size, True)
        self.text = text
        self.color = color
        self.pos = pos

    def draw(self, text, screen):
        text_surface = self.font.render(text, True, self.color)
        screen.blit(text_surface, self.pos)

# Score
score = 0
score_text = Text("Score: "+str(score), 32, (10,10))

# Sound
explosion_sound = pygame.mixer.Sound("assets/explosion.wav")
laser_sound = pygame.mixer.Sound("assets/laser.wav")

# background music
pygame.mixer.music.load("assets/background.wav")
pygame.mixer.music.play(-1) # -1 to run indefinitely

# player
p = Player()

# bullet
b = Bullet(p.x) 

# enemy
num_enemies = 5
es = [] # list of enemy object
for i in range(num_enemies):
    e = Enemy()
    e.respawn()
    es.append(e)

def gameover(screen, score):

    over_text = Text("GAME OVER!!", 74, (150,200))
    score_text = Text("Final Score: "+str(score), 34, (300,300))
    message = Text("Press Q to Quit", 20, (300, 400))
    
    run = True
    while run:
        screen.fill((0,0,0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.KEYDOWN and event.key == pygame.K_q:
                run = False

        over_text.draw("GAME OVER!!", screen)
        score_text.draw("Final Score: "+str(score), screen)
        message.draw("Press Q to Quit", screen)

        pygame.display.update()



run = True
while run:
    screen.fill((0,0,0))
    # screen.blit(background_img, (0,0)) # for inserting background image

    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                p.xvel = -5
                print("LEFT")

            if event.key == pygame.K_RIGHT:
                p.xvel = 5
                print("RIGHT")

            if event.key == pygame.K_SPACE:
                print("SPACE")
                if b.state == "ready":
                    b.state = "fired"
                    laser_sound.play()


        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                p.xvel = 0
                print("KEY RELEASED")

    
    
    p.move()
    b.move(p.x)

    for e in es:
        e.move()
        collision = b.collide(e)
        if collision:
            explosion_sound.play()
            e.respawn()
            b.respawn(p.x)
            score += 1


        # gameover
        if e.y >= 386:
            gameover(screen, score)
            run = False
             
    
    for e in es:
        e.draw(screen)
    score_text.draw("Score: "+str(score), screen)
    b.draw(screen)
    p.draw(screen)
    pygame.display.update()