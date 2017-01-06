import sys
import pygame

YELLOW = 255, 255, 0
BLACK = 0, 0, 0
WHITE = 255, 255, 255 
BLUE = 0, 0, 255

class Scene:

    def __init__(self, size=(640, 480)):
        pygame.init()
        self.items = []
        self.width = size[0]
        self.high = size[1]
        self.size = size
        self.screen = pygame.display.set_mode(self.size)
        self.last_key = None

    def add(self, item):
        self.items.append(item)

    def clear(self):
        self.items.clear()

    def get_keys(self):
        pressed = pygame.key.get_pressed()
        pressed_wasd = []
        if pressed[pygame.K_w]:
            pressed_wasd.append("w")
        if pressed[pygame.K_a]:
            pressed_wasd.append("a")
        if pressed[pygame.K_s]:
            pressed_wasd.append("s")
        if pressed[pygame.K_d]:
            pressed_wasd.append("d")

        return pressed_wasd

    def draw(self):
        self.screen.fill(WHITE)
        for item in self.items:
            item.draw(self.screen) 
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()
        
  
class Circle:
    def __init__(self,center,radius,color=YELLOW):
        self.surf = pygame.Surface((2*radius, 2*radius))
        self.surf.set_colorkey(WHITE)
        self.surf.fill(WHITE)
        self.rect = pygame.draw.circle(self.surf, color, (radius, radius), radius)
        self.rect = self.rect.move(int(center[0]), int(center[1]))

    def draw(self, screen):
        screen.blit(self.surf, self.rect)

def test():
    pygame.init()
    WORLD_SIZE = width, height = 1024, 768 
    BALL_SIZE = 50

    speed = [1, 1]
    
    screen = pygame.display.set_mode(WORLD_SIZE)
    
    ball = pygame.Surface((BALL_SIZE, BALL_SIZE))
    ballrect = pygame.draw.circle(ball, BLUE, (BALL_SIZE//2, BALL_SIZE//2), BALL_SIZE//2)
    
    #for j in range(1000):
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()
    
        ballrect = ballrect.move(speed)
        if ballrect.left < 0 or ballrect.right > width:
            speed[0] = -speed[0]
        if ballrect.top < 0 or ballrect.bottom > height:
            speed[1] = -speed[1]
    
        screen.fill(BLACK)
        screen.blit(ball, ballrect)
        pygame.display.flip()
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()

def test2():
    sceene = Scene((640, 480))
    sceene.add(Circle((40,50),10))
    sceene.add(Circle((140,50),10))

    key = None
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()

        sceene.draw()
        key = sceene.get_keys()

if __name__ == '__main__':
    test2()
