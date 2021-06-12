from model.files import getImage
from model.fractal import drawTree
from model.tree import Tree
from model.genetic import generate_pob, test_pob, merge
from view.window import Window
import math
import numpy as np
import pygame
import sys
import time
import easygui
import ntpath
from pygame.locals import *
import numpy as np
from view.sprite import *


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

        self.screen = pygame.display.set_mode((800, 800))
        self.screen.fill((137, 207, 240))
        self.pygame.display.set_caption("Fractal Tree")

        self.sprite1 = Sprite("Arrow.png", 200, 400, 0, 0)

        self.Font = self.pygame.font.SysFont('comicsans', 30)
        self.text = self.Font.render('Seleccione la imagen a utilizar', True, (0,0,0))
        self.text_rect = self.text.get_rect()
        self.text_rect.center = (800 / 5,800 / 5)
        self.screen.blit(self.text, self.text_rect)

        self.flag=False
        self.file="Frame 3.png"


    # Override
    # D: Dibuja la GUI
    def draw_gui(self, event):

        BLACK=(0,0,0)
        RED=(255,0,0)

        self.text = self.Font.render('Seleccione la imagen a utilizar', True, BLACK)

        color=BLACK

        mouse_pos = (0,0)
        mouse_click = (0,0)

        if self.text_rect.collidepoint(self.pygame.mouse.get_pos()):
            self.text = self.Font.render('Seleccione la imagen a utilizar', True, (255,0,0))

        if event.type==MOUSEBUTTONUP:
            if self.text_rect.collidepoint(self.pygame.mouse.get_pos()):
                self.file = easygui.fileopenbox()
                self.file= ntpath.basename(self.file)
                self.flag=True
                print(self.file)

        self.screen.blit(self.text, self.text_rect)



    # Override
    def start_game(self):
        self.is_running = True

        self.append_event(self.draw_gui)
        self.append_event(self.draw_tree)
        self.append_render(self.render_queue)
        
        self.game_loop()

    def set_area(self):

        self.tree = self.pygame.image.load(self.file)
        self.img = getImage(self.file)

        self.totalArea = [0, 0, len(self.img)]

        for x in range(len(self.img)):
            for y in range(len(self.img[0])):
                isWhite = np.sum(self.img[y][x]) == 4
                if not isWhite and y < self.totalArea[2]:
                    self.totalArea[2] = y

                self.totalArea[isWhite] += 1
        print(self.totalArea[2])

        return [self.totalArea,self.img]

    def render_queue(self):

        if len(self.tree_list) == 0:
            return

        self.screen.blit(self.tree, (200, 400))

        origin = [200, 400]
        matrix = np.zeros((200, 200), dtype=int)

        drawTree(self.tree_list[0], self.screen, self.img, origin, matrix, shouldRender = True)

        self.tree_list.pop(0)
        time.sleep(0.1)

    # E/S: N/A
    # D: Se encarga de hacer la animacion del cursor
    def animate_cursor(self):



        cursor = self.__pygame.Rect(self.pygame.mouse.get_pos())

        start_pos = (self.pygame.mouse.get_pos())
        end_pos = (self.pygame.mouse.get_pos())

        time_since = time.time() * 1000.0 - self.__cursor_time

        if time_since <= 500:
            self.__pygame.draw.line(
                self.screen, COLOR_WHITE, start_pos, end_pos, 3)
        elif 500 < time_since and time_since <= 1000:
            self.__pygame.draw.line(
                self.screen, (0, 0, 0), start_pos, end_pos, 3)
        else:
            self.main_clock = time.time() * 1000

    # D: Dibuja un arbol en pantalla
    def draw_tree(self, event):

        print(self.flag ,"--",self.file)

        if self.flag==False:
            return

        if event.type != self.pygame.KEYDOWN:
            return

        if event.key != self.pygame.K_SPACE:
            return

        aux=self.set_area()
        self.totalArea=aux[0]
        self.img=aux[1]

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