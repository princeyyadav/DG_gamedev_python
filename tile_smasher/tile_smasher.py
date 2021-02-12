import pygame, random
pygame.init()

class Image:

    def __init__(self, path, pos):
        self.image = pygame.image.load(path) # image is Surface
        self.pos = pos

    def draw(self, screen):
        screen.blit(self.image, self.pos)

class Button:

    def __init__(self, surface, pos):
        self.image = surface # pygame Surface
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]

    def mousehover(self, mpos):
        return self.rect.collidepoint(mpos)

    def draw(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))


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
        self.image = self.font.render(self.text, True, self.color) # image is a pygame Surface object
    
    def update(self, text):
        self.text = text
        self.render()

    def draw(self, screen):
        screen.blit(self.image, self.pos)

class Tile:

    def __init__(self, width, height, color):
        self.image = pygame.Surface((width, height))
        self.image.fill(color)
        self.rect = self.image.get_rect() # x, y -> (0,0)
        self.respawn()

    def respawn(self):
        self.rect.x = random.randint(10, 800-self.rect.width)
        self.rect.y = random.randint(10, 600-self.rect.height)

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def mousehover(self, mpos):
        return self.rect.collidepoint(mpos)
        
def gameover(screen, score):

    run = True
    gameover = Text("GAMEOVER!!", 50, (300,200))
    score_txt = Text("SCORE: "+str(score), 50, (340, 300))
    while run:

        screen.fill(BLACK)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        gameover.draw(screen)
        score_txt.draw(screen)
        pygame.display.update()

def arcade(screen):

    life = 10
    heart = Image("assets/heart.png", (800-10-32, 10))

    # tile 
    tile = Tile(100,100, RED)
    start = pygame.time.get_ticks()

    score = 0
    score_txt = Text("Score: 0", 32, (10,10))

    run = True
    while run:

        clicked = False # clicked on tile or not

        screen.fill(BLACK)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False


            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mpos = pygame.mouse.get_pos()
                if tile.mousehover(mpos):
                    clicked = True
                    tile.respawn()
                    score += 1
                    score_txt.update("Score: "+str(score))
                    start = pygame.time.get_ticks()

        if pygame.time.get_ticks() - start >= 1000:
            tile.respawn()
            start = pygame.time.get_ticks()
            if not(clicked):
                life -= 1
                print(life)

        # gameover
        if life <= 0:
            print("GAMEOVER")
            gameover(screen, score)
            run = False

        for i in range(life):
            heart.pos = (758-35*i, 10)
            heart.draw(screen)
        score_txt.draw(screen)
        tile.draw(screen)
        pygame.display.update()

def timeout(screen):

    # tile 
    tile = Tile(100,100, RED)
    run = True
    start = pygame.time.get_ticks() # gives time in ms
    gamestart = pygame.time.get_ticks()
    
    # score
    score = 0
    score_txt = Text("Score: 0", 32, (10,10))

    while run:

        screen.fill(BLACK)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mpos = pygame.mouse.get_pos()
                if tile.mousehover(mpos):
                    score += 1
                    score_txt.update("Score: "+str(score))
                    print(score)
                    tile.respawn()
                    start = pygame.time.get_ticks()

        if pygame.time.get_ticks() - start >= 1000: # 1 sec has been lapsed
            tile.respawn()
            start = pygame.time.get_ticks()

        # gameover
        if pygame.time.get_ticks() - gamestart >= 10000:
            print("GAMEOVER")
            run = False
            gameover(screen, score)

        score_txt.draw(screen)
        tile.draw(screen)
        pygame.display.update()

    run 
# colors
BLACK = (0,0,0)
WHITE = (255,255, 255)
RED = (219, 0, 0)

w, h = 800, 600
screen = pygame.display.set_mode((w,h))
pygame.display.set_caption("TILE SMASHER")


title_txt = Text("Tile Smasher", 64, (250,100))
select_txt = Text("Select Mode:", 32, (20,200))
timeout_txt = Text("Time-Out", 32, (340, 300))
arcade_txt = Text("Arcade", 32, (350, 350))
start_txt = Text("Start", 40, (370,450))

timeout_btn = Button(timeout_txt.image, timeout_txt.pos)
arcade_btn = Button(arcade_txt.image, arcade_txt.pos)
start_btn = Button(start_txt.image, start_txt.pos)

mode = 0
run = True
while run:

    screen.fill(BLACK)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mpos = pygame.mouse.get_pos()
            if timeout_btn.mousehover(mpos):
                mode = 1

            elif arcade_btn.mousehover(mpos):
                mode = 2

            elif start_btn.mousehover(mpos) and mode:
                print("START", mode)
                if mode==1:
                    timeout(screen)
                else:
                    arcade(screen)

    if mode == 1:
        rect = pygame.Rect(timeout_btn.rect.x - 10, timeout_btn.rect.y - 10, timeout_btn.rect.width+20, timeout_btn.rect.height+20)
        pygame.draw.rect(screen, RED, rect, 3)

    elif mode == 2:
        rect = pygame.Rect(arcade_btn.rect.x - 10, arcade_btn.rect.y - 10, arcade_btn.rect.width+20, arcade_btn.rect.height+20)
        pygame.draw.rect(screen, RED, rect, 3)
       

    title_txt.draw(screen)
    select_txt.draw(screen)

    timeout_btn.draw(screen)
    arcade_btn.draw(screen)
    start_btn.draw(screen)
    pygame.display.update()

    