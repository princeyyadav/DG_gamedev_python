import pygame, random
pygame.init()

class Image:

    def __init__(self, path, pos):
        self.image = pygame.image.load(path) # image is Surface
        self.pos = pos

    def draw(self, screen):
        screen.blit(self.image, self.pos)

class Button:

    def __init__(self, path, pos):
        self.image = pygame.image.load(path) # image is Surface
        self.rect = self.image.get_rect() # x, y = (0,0)
        self.rect.x = pos[0]
        self.rect.y = pos[1]

    def mousehover(self, mpos):
        # if self.rect.x <= mpos[0] <= self.rect.x + self.rect.width and self.rect.y <= mpos[1] <= self.rect.y + self.rect.height:
        #     return True
        # return False
        return self.rect.collidepoint(mpos)

    def draw(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))

class Bucket(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("assets/bucket.png")
        self.rect = self.image.get_rect()

    def move(self, mpos):
        self.rect.x = mpos[0]
        self.rect.y = mpos[1]

class Coin(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("assets/s_coin.png")
        self.rect = self.image.get_rect() # rect.x, rect.y -> (0,0)
        self.yvel = 10
        self.respawn()

    def respawn(self):
        self.rect.x = random.randint(0, 800-self.rect.width)
        self.rect.y = random.randint(-800, -50)

    def move(self):
        self.rect.y += self.yvel

        if self.rect.top >= 600:
            self.respawn()


class Text:

    def __init__(self, text, size, pos, fontname="Arial", color=(255,255,255)):
        self.text = text
        self.pos = pos
        
        self.fontname = fontname
        self.size = size
        self.color = color
        self.set_font()
        self.render()

    def set_font(self):
        self.font = pygame.font.SysFont(self.fontname, self.size, True)

    def render(self):
        """ render the text into an image/ Surface """
        self.image = self.font.render(self.text, True, self.color)
    
    def update(self, text):
        self.text = text
        self.render()

    def draw(self, screen):
        screen.blit(self.image, self.pos)

def gameover(screen):

    gameover = Image("assets/Game-Over.png", (250, 200))

    run = True
    while run:

        screen.fill((0,0,0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        gameover.draw(screen)
        pygame.display.update()

        
    

def maingame(screen):

    b = Bucket()
    sprites = pygame.sprite.Group() # it stores all the game sprites
    sprites.add(b)

    num_coins = 50
    coins = pygame.sprite.Group() # stores only coin sprites

    for i in range(num_coins):
        c = Coin()
        sprites.add(c) # add coin sprite to the Group
        coins.add(c)

    # sound 
    coin_sound = pygame.mixer.Sound("assets/collect_coin.wav")

    FPS = 40
    clock = pygame.time.Clock()

    # score
    score = 0
    score_txt = Text("Score: 0", 32, (10, 10))

    ticks = 0 # counter

    # countdown
    count = 10
    countdown_txt = Text(str(count), 50, (760,10))

    run = True
    while run:

        screen.fill(pygame.Color("grey12")) # pygame.Color("grey12") -> RGB value
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        # bucket move
        mpos = pygame.mouse.get_pos()
        b.move(mpos)

        # coin move
        for c in coins:
            c.move()

        coins_collected = pygame.sprite.spritecollide(b, coins, False) # collision b/w bucket & coins Group
        for c in coins_collected:
            c.respawn()
            score += 1
            score_txt.update("Score: "+str(score)) # update the text attribute of score_txt
            coin_sound.play()

        # gameover
        ticks += 1
        if ticks >= FPS*10: # 10 sec lapsed
            print("gameover")
            gameover(screen)
            run = False

        # countdown
        if ticks%FPS == 0:
            count -= 1
            countdown_txt.update(str(count)) # update countdown text attribute

        countdown_txt.draw(screen)
        score_txt.draw(screen)
        sprites.draw(screen)
        pygame.display.update()



w,h = 800, 600
screen = pygame.display.set_mode((w,h)) # screen is a Surface
pygame.display.set_caption("COLLECT THE COINS")

icon = pygame.image.load("assets/coin.png") # icon is Surface object
pygame.display.set_icon(icon)

title = Image("assets/Collect-the-Coins.png",(50, 250))
start_btn = Button("assets/Start.png", (400, 400))

run = True
while run:

    screen.fill((0,0,0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1: # Left click
                print("LEFT BUTTON CLICKED")
                mpos = pygame.mouse.get_pos() # gives cursor position, mpos->(x,y)
                if start_btn.mousehover(mpos):
                    maingame(screen)
                
    
    title.draw(screen)
    start_btn.draw(screen)
    pygame.display.update()
