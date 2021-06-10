from model.files import getImage
from model.fractal import drawTree
from model.tree import Tree
from model.genetic import generate_pob, test_pob, merge
from view.window import Window
import math
import numpy as np

import pandas as pd
import time

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

        self.tree_list = []
        
        self.click = False
        self.main_clock = pygame.time.Clock()

        self.screen = pygame.display.set_mode((600, 600))
        self.pygame.display.set_caption("Fractal Tree")

    # Override
    def start_game(self):
        self.is_running = True

        self.tree = self.pygame.image.load("Frame 3.png")
        self.img = getImage("Frame 3.png")

        self.totalArea = [0, 0, len(self.img)]

        for x in range(len(self.img)):
            for y in range(len(self.img[0])):
                isWhite = np.sum(self.img[y][x]) == 4
                if not isWhite and y < self.totalArea[2]:
                    self.totalArea[2] = y

                self.totalArea[isWhite] += 1
        print(self.totalArea[2])

        self.append_event(self.draw_tree)
        self.append_render(self.render_queue)

        self.game_loop()

    def render_queue(self):
        if len(self.tree_list) == 0:
            return

        self.screen.fill((0, 0, 0))
        self.screen.blit(self.tree, (200, 400))

        origin = [200, 400]
        matrix = np.zeros((200, 200), dtype=int)

        drawTree(self.tree_list[0], self.screen, self.img, origin, matrix, shouldRender = True)

        self.tree_list.pop(0)
        time.sleep(0.1)

    # D: Dibuja un arbol en pantalla
    def draw_tree(self, event):
        if event.type != self.pygame.KEYDOWN:
            return

        if event.key != self.pygame.K_SPACE:
            return

        origin = [200, 400]

        population = generate_pob(100)

        data = pd.DataFrame([], columns = ['num_individuo', 'generacion', 'fitness'])

        for i in range(0, 10):
            print("Generacion #", i)

            pob = test_pob(population, self.totalArea, self.img, origin)

            print("Fitness: ", pob[0][0])
            print(pob[0][1])

            matrix = np.zeros((200, 200), dtype=int)
            #drawTree(pob[0][1], self.screen, self.img, origin, matrix, shouldRender = True)
            self.tree_list.append(pob[0][1])
            result = []

            for k in range(len(pob)):
                row = pd.DataFrame([[k, i+1, pob[k][0]]], columns = ['num_individuo', 'generacion', 'fitness'])

                data.append(row)

                data = data.append(row)
                result.append(pob[0][1])

            population = merge(result)

        rst = data.to_csv('resultados.csv', index=False)

        #drawTree(pob[0][1], self.screen, self.img, origin, matrix, shouldRender = True)
        print("Mejor")
        print(pob[0][1])