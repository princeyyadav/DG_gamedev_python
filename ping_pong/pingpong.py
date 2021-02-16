import pygame, random
pygame.init()

# colors
RED = (220, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (237, 186, 0)
GREY = (130, 130, 130)

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


def maingame(screen, level, total_balls=10):
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        pygame.display.update()

w, h = 800, 600
screen = pygame.display.set_mode((w,h))
pygame.display.set_caption("PING PONG")
icon = pygame.image.load("assets/ping-pong.png")
pygame.display.set_icon(icon)

title = Text("PING PONG", 50, (300, 60))
levels = Text("SELECT LEVELS", 40, (50,160))

easy = Text("EASY", 32, (380, 260))
medium = Text("MEDIUM", 32, (360, 310))
hard = Text("HARD", 32, (380, 360))

easy_btn = Button(easy.image, (380, 260))
medium_btn = Button(medium.image, (360, 310))
hard_btn = Button(hard.image, (380, 360))

num_balls = Text("NO. OF BALLS", 40, (50,440))
inp_rect = pygame.Rect(340, 430, 200, 60) # text box

start = Text("START", 40, (370, 520))
start_btn = Button(start.image, (370, 520))

inp = ""
level = 0
run = True
while run:

    screen.fill(pygame.Color("grey12"))

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mpos = pygame.mouse.get_pos()
            if easy_btn.mousehover(mpos):
                level = 1
            elif medium_btn.mousehover(mpos):
                level = 2
            elif hard_btn.mousehover(mpos):
                level = 3
            elif start_btn.mousehover(mpos) and level:
                maingame(screen, level)
                print("START CLICKED", level)

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                print("BACKSPACE")
                inp = inp[:-1]
            elif event.key == pygame.K_RETURN: # enter key
                print("ENTER")
            else:
                inp += event.unicode

    if inp:
        text = Text(inp, 40, (inp_rect.x+10, inp_rect.y+5), color = YELLOW)
    else:
        text = Text("Enter balls here.", 25, (inp_rect.x+10, inp_rect.y+15), color = GREY)

    text.draw(screen)

    if level == 1:
        rect = pygame.Rect(easy_btn.rect.x-10, easy_btn.rect.y-10, easy_btn.rect.width+20, easy_btn.rect.height+20)
        pygame.draw.rect(screen, YELLOW, rect, 3, 10)
    elif level == 2:
        rect = pygame.Rect(medium_btn.rect.x-10, medium_btn.rect.y-10, medium_btn.rect.width+20, medium_btn.rect.height+20)
        pygame.draw.rect(screen, YELLOW, rect, 3, 10)
    elif level == 3:
        rect = pygame.Rect(hard_btn.rect.x-10, hard_btn.rect.y-10, hard_btn.rect.width+20, hard_btn.rect.height+20)
        pygame.draw.rect(screen, YELLOW, rect, 3, 10)
        


    title.draw(screen)
    levels.draw(screen)
    easy_btn.draw(screen)
    medium_btn.draw(screen)
    hard_btn.draw(screen)

    num_balls.draw(screen)

    pygame.draw.rect(screen, WHITE, inp_rect, 3)

    start_btn.draw(screen)
    pygame.display.update()

