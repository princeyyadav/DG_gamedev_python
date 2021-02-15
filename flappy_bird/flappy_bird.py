import pygame, random
pygame.init()

# colors
BLACK = (0,0,0)
WHITE = (255, 255, 255)
SKYBLUE = (112, 207, 244)

class Bird:

    def __init__(self, pos):
        self.image = pygame.image.load("images/bird.png")
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = pos
        self.yvel = 6
        self.fly = False

    def draw(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))

    def move(self):
        if self.fly:
            self.rect.y -= self.yvel
        else:
            self.rect.y += self.yvel

        if self.rect.y <= 0:
            self.rect.y = 0
        if self.rect.bottom >= 400:
            self.rect.bottom = 400

    def collide(self, p):
        return self.rect.colliderect(p.trect) or self.rect.colliderect(p.brect)

class Pipes:

    def __init__(self, pos):
        self.top = pygame.image.load("images/pipe-up.png")
        self.bottom = pygame.image.load("images/pipe-down.png")
        self.trect = self.top.get_rect()
        self.brect = self.bottom.get_rect()
        self.trect.x, self.trect.y = pos
        self.brect.x, self.brect.y = pos[0], pos[1]+320+100
        self.vel = 10

    def draw(self, screen):
        screen.blit(self.top, self.trect)
        screen.blit(self.bottom, self.brect)

    def move(self):
        self.trect.x -= self.vel
        self.brect.x -= self.vel

        global score

        if self.trect.x <= -self.trect.width:
            self.trect.x = 300
            self.brect.x = 300
            self.trect.y = random.randint(-200, -100)
            self.brect.y = self.trect.y + 320 + random.randint(100, 120)
            score += 1

        
def gameover(screen):

    gameover = pygame.image.load("images/gameover.png")
    run = True
    while run:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        screen.blit(gameover, (60,250))
        pygame.display.update()

def display_score(score, font, screen):
    image = font.render(str(score), True, WHITE)
    screen.blit(image, (10, 10))

def game(screen):

    bg = pygame.image.load("images/background.png")
    bg = pygame.transform.scale(bg, (w,h))
    # bg_rect = bg.get_rect()
    # print(bg_rect.width, bg_rect.height)

    base = pygame.image.load("images/base.png")

    # bird
    b = Bird((50,250))

    # pipes
    pipes = []
    pipe_pos = [[200, -100], 
                [400, -140]]

    for pos in pipe_pos:        
        p = Pipes(pos)
        pipes.append(p)

    FPS = 30
    clock = pygame.time.Clock()

    # score
    global score
    score = 0
    font = pygame.font.SysFont("Arial", 32, True)

    run = True
    while run:
        
        screen.blit(bg, (0,0))
        clock.tick(FPS)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                b.fly = True
                # print("SPACE")

            if event.type == pygame.KEYUP and event.key == pygame.K_SPACE:
                b.fly = False
                # print("RELEASED")

        b.move()
        for p in pipes:
            p.move()
            if b.collide(p):
                print("GAMEOVER")
                gameover(screen)
                run = False

        for p in pipes:    
            p.draw(screen)
        b.draw(screen)
        display_score(score, font, screen)
        screen.blit(base, (0, 400))
        pygame.display.update()

    

w, h = 300, 500
screen = pygame.display.set_mode((w, h))
pygame.display.set_caption("FLAPPY BIRD")

icon = pygame.image.load("images/bird.png")
pygame.display.set_icon(icon)

welcome_bg = pygame.image.load("images/intro.png")
# welcome_bg = pygame.transform.scale(welcome_bg, (w,h)) # scale to screen dim

bg_rect = welcome_bg.get_rect()

print(bg_rect.width, bg_rect.height)

run = True
while run:

    screen.fill(SKYBLUE)
    screen.blit(welcome_bg, (60,120)) # draw

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            print("TAP")
            game(screen)

    pygame.display.update()

    
