from pygame.locals import *

class Slider():
    data = []
    arrows = [None, None]
    bg = None
    state = None
    cursor = 0
    screen = None
    position = (0, 0)
    pygame = None
    color = (255, 255, 255)

    # E: Una lista con imagenes de flechas
    #    Una lista con los datos
    #    Una referencia a una pantalla de Python
    def __init__(self, arrows, data, screen, pygame, position = (0, 0)):
        self.arrows = arrows[:2]
        self.bg = arrows[2]
        self.screen = screen
        self.state = data[self.cursor]
        self.position = position
        self.pygame = pygame
        self.data = data

        self.font = self.pygame.font.SysFont('default', 30)

    # Renderiza los datos
    def render(self):
        # Va a estar 250px de la flecha izquierda
        rightArrowsPos = (self.position[0] + 220, self.position[1])
        
        bgPos = (self.position[0] + 20, self.position[1])
        
        self.screen.blit(self.arrows[0], self.position)
        self.screen.blit(self.arrows[1], rightArrowsPos)
        self.screen.blit(self.bg, bgPos)

        text = self.font.render(str(self.data[self.cursor]), True, (0,0,0))
        text_rect = text.get_rect()
        text_rect.center = (self.position[0]+20 + 200/2, self.position[1] + 60/2)

        self.screen.blit(text, text_rect)

    def events(self, event):
        if event.type != MOUSEBUTTONUP:
            return 

        leftArrowPos = [self.position, (self.position[0] + 20, self.position[1] + 60)]
        rightArrowPos = [(self.position[0] + 220, self.position[1]), (self.position[0] + 240, self.position[1] + 60)]
        
        print(self.pygame.mouse.get_pos())
        print(rightArrowPos)
        if self.didCollide(leftArrowPos, self.pygame.mouse.get_pos()):
            self.cursor -= 1
        
        if self.didCollide(rightArrowPos, self.pygame.mouse.get_pos()):
            self.cursor += 1

        self.cast()

    def setData(self, data):
        self.data = data
        self.cursor = 0

    def getState(self):
        return self.cursor

    def cast(self):
        if self.cursor >= len(self.data):
            self.cursor = 0
        
        if self.cursor < 0:
            self.cursor = len(self.data) - 1

    def didCollide(self, rect, point):
        if rect[0][0] > point[0] or point[0] > rect[1][0]:
            return False

        return rect[0][1] <= point[1] + 10 and point[1] + 10 <= rect[1][1]

        