from model.files import getImage
from model.fractal import drawTree
from model.tree import Tree
from model.genetic import generate_pob, test_pob, merge
from view.window import Window
import math
import numpy as np

# Desc: Esto requiere un mejor diseño, probablemente lo refactorice más adelante
# Clase que contiene la ventana del home
class Home(Window):
    # E: Una referencia a Pygame
    # Desc: Constructor de la clase
    def __init__(self, pygame):
        self.pygame = pygame
        self.is_running = False

        self.render_list = []
        self.events = []
        
        self.click = False
        self.main_clock = pygame.time.Clock()

        self.screen = pygame.display.set_mode((600, 600))
        self.pygame.display.set_caption("Fractal Tree")

    # Override
    def start_game(self):
        self.is_running = True

        self.tree = self.pygame.image.load("Frame 4.png")
        self.img = getImage("Frame 4.png")

        self.totalArea = [0, 0, len(self.img)]

        for x in range(len(self.img)):
            for y in range(len(self.img[0])):
                isBlack = np.sum(self.img[y][x]) == 4
                if not isBlack and y < self.totalArea[2]:
                    self.totalArea[2] = y

                self.totalArea[isBlack] += 1
        print(self.totalArea[2])
        self.append_event(self.draw_tree)

        self.game_loop()

    # D: Dibuja un arbol en pantalla
    def draw_tree(self, event):
        if event.type != self.pygame.KEYDOWN:
            return

        if event.key != self.pygame.K_SPACE:
            return

        origin = [200, 400]

        population = generate_pob(50)

        for i in range(0, 10):
            self.screen.fill((0, 0, 0))
            self.screen.blit(self.tree, (200, 400))

            print("Generacion #", i)

            pob = test_pob(population, self.totalArea, self.img, origin)

            print("Fitness: ", pob[i][0])
            print(pob[i][1])

            matrix = np.zeros((200, 200), dtype=int)
            drawTree(pob[0][1], self.screen, self.img, origin, matrix, shouldRender = True)

            result = []

            for i in range(len(pob)):
                result.append(pob[i][1])

            population = merge(result)

        print("Mejor")
        print(pob[0][1])