import pygame 
from pygame.locals import * 


SCREEN_SIZE = (800, 600)
TILE_SIZE = 32

def toSCRCoord(x,y):
    return(x-y,(x+y)/2)
def render(object,screen):
    screen.blit(object.image, toSCRCoord(object.rect.x,object.rect.y))
    
class Tile():
    def __init__(self,x,y):
        self.image = pygame.image.load("tile.png")
        self.rect = self.image.get_rect()
        self.rect.x = x * TILE_SIZE
        self.rect.y = y * TILE_SIZE
        
        
class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode(SCREEN_SIZE)
        self.clock = pygame.time.Clock()
        
    def loadLVL(self,map ):
        f = open(map.txe, "r")
        data = f.readlines()
        print(data)
    
    def events(self):
        for event in pygame.event.get():
            if event.type == quit:
                quit
                
    def renderSCR(self):
        self.screen.fill("sky blue")
        pygame.display.update()

    def update(self):#every frame 
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    
            self.events()
            self.renderSCR()
    
    def start(self):#first frame
        self.loadLVL("map.txt")
    
    def main(self):#whot runs the game 
        self.start()
        self.update()
        
g = Game()
g.main()
pygame.quit()
  