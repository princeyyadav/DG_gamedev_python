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

    def respawn(self):
        self.trect.x = 300
        self.brect.x = 300
        self.trect.y = random.randint(-200, -100)
        self.brect.y = self.trect.y + 320 + random.randint(100, 120)

    def move(self):
        self.trect.x -= self.vel
        self.brect.x -= self.vel
        if self.trect.x <= -(self.trect.width):
            self.respawn()


def gameover(screen, score, base, bird, pipes):

    gameover = pygame.image.load("images/gameover.png")
    gameover.set_colorkey(BLACK) # make BLACK color transparent

    font = pygame.font.SysFont("Arial", 35, True)
    score_image = font.render("SCORE: "+str(score), True, (50, 50, 50))

    run = True
    while run:

        screen.fill(SKYBLUE)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
  
        
        bird.draw(screen)
        for p in pipes:
            p.draw(screen)
        screen.blit(base, (0,400))
        screen.blit(gameover, (60,150))
        screen.blit(score_image, (90, 210))
        pygame.display.update()

def display_score(score, font, screen):
    image = font.render(str(score), True, WHITE)
    screen.blit(image, (10, 10))

def update_score(score, p):
    if p.trect.x <= -(p.trect.width-2): # -width & -width+1 didn't work
        score += 1
        print(score)
        point_sound.play()
    return score

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
    score = 0
    font = pygame.font.SysFont("Arial", 40, True)

    run = True
    while run:
        
        screen.blit(bg, (0,0))
        clock.tick(FPS)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                b.fly = True
                wing_sound.play()
                # print("SPACE")

            if event.type == pygame.KEYUP and event.key == pygame.K_SPACE:
                b.fly = False
                # print("RELEASED")

        b.move()
        for p in pipes:
            p.move()
            score = update_score(score, p)
            if b.collide(p):
                die_sound.play()
                gameover(screen, score, base, b, pipes)
                run = False

        b.draw(screen)
        for p in pipes:    
            p.draw(screen)
        screen.blit(base,(0, 400))
        display_score(score, font, screen)
        pygame.display.update()


# sounds
die_sound = pygame.mixer.Sound("sounds/die.wav")
point_sound = pygame.mixer.Sound("sounds/point.wav")
wing_sound = pygame.mixer.Sound("sounds/wing.wav")    

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

    
