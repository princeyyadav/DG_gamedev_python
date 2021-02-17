import pygame
import socket
pygame.init()

RED = (220, 0, 0)
GREEN = (40, 143, 0)

class Network:

    def __init__(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = "192.168.0.103"
        self.port = 5555
        self.addr = (self.server, self.port)
        self.pos = self.connect()

    def connect(self):
        self.s.connect(self.addr) # connect to the socket at given address
        return self.s.recv(4096).decode()

    def send(self, data):
        self.s.send(str.encode(data))
        return self.s.recv(4096).decode()

class Player:

    def __init__(self, x, y, w, h, color):
        self.image = pygame.Surface((w,h))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y
        self.vel = 3

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def move(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.vel
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.vel
        if keys[pygame.K_UP]:
            self.rect.y -= self.vel
        if keys[pygame.K_DOWN]:
            self.rect.y += self.vel

        if self.rect.x <= 0:
            self.rect.x = 0
        elif self.rect.right >= w:
            self.rect.right = w
        
        if self.rect.y <= 0:
            self.rect.y = 0
        elif self.rect.bottom >= h:
            self.rect.bottom = h

def make_str(tup):
    return str(tup[0])+","+str(tup[1])

def make_tuple(st):
    st = st.split(",")
    return int(st[0]), int(st[1])
    

w, h = 500, 500
screen = pygame.display.set_mode((w,h))
caption = "CLIENT"
pygame.display.set_caption(caption)

# Network object
n = Network()
x, y = make_tuple(n.pos) # coordinates receiced from server

# player
p = Player(x, y, 100, 100, RED)
p2 = Player(0, 0, 100, 100, GREEN)

FPS = 30
clock = pygame.time.Clock()

run = True
while run:

    screen.fill((255, 255, 255))
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False    
    
    p.move()

    # send updated coordinates  to the server
    data = make_str((p.rect.x, p.rect.y))   
    p2_pos = make_tuple(n.send(data))
    p2.rect.x = p2_pos[0]
    p2.rect.y = p2_pos[1]


    p2.draw(screen)
    p.draw(screen)
    pygame.display.update()



