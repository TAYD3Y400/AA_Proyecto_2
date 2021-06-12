import numpy as np
import easygui
import ntpath
import pygame
import math
import time
import sys

from model.genetic import generate_pob, test_pob, merge
from model.fractal import drawTree
from model.files import getImage
from view.slider import Slider
from view.window import Window
from model.tree import Tree
from pygame.locals import *
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
        
        self.trees_per_gen = {}
        
        self.click = False
        self.main_clock = pygame.time.Clock()

        self.execute_state = (255, 0, 0)

        self.screen = pygame.display.set_mode((800, 800))
        self.screen.fill((137, 207, 240))
        self.pygame.display.set_caption("Fractal Tree")

        self.sprite1 = Sprite("Arrow.png", 200, 400, 0, 0)

        self.Font = self.pygame.font.SysFont('default', 30)
        self.text = self.Font.render('Seleccione la imagen a utilizar', True, (0,0,0))
        self.text_rect = self.text.get_rect()
        self.text_rect.center = (800 / 5,800 / 5)
        self.screen.blit(self.text, self.text_rect)

        self.flag=False
        self.file="Frame 3.png"

        self.leftArrow = self.pygame.image.load("FlechaIzq.png")
        self.rightArrow = self.pygame.image.load("FlechaDer.png")
        self.sliderBG = self.pygame.image.load("Rect.png")

        self.genSlider = Slider([self.leftArrow, self.rightArrow, self.sliderBG], np.arange(1), self.screen, self.pygame, position=(0, 60))

    # Override
    def start_game(self):
        self.is_running = True

        self.append_event(self.draw_gui)
        self.append_event(self.genSlider.events)
        self.append_event(self.draw_tree)

        self.append_render(self.genSlider.render)
        self.append_render(self.render_queue)
        
        self.game_loop()

    # D: Dibuja la GUI
    def draw_gui(self, event):
        BLACK=(0,0,0)
        RED=(255,0,0)

        self.text = self.Font.render('Seleccione la imagen a utilizar', True, BLACK)

        color=BLACK

        mouse_pos = (0,0)
        mouse_click = (0,0)

        if self.text_rect.collidepoint(self.pygame.mouse.get_pos()):
            self.text = self.Font.render('Seleccione la imagen a utilizar', True, RED)

        if event.type==MOUSEBUTTONUP:
            if self.text_rect.collidepoint(self.pygame.mouse.get_pos()):
                self.file = easygui.fileopenbox()
                self.file= ntpath.basename(self.file)
                self.flag=True
                print(self.file)

        self.draw_circle_state()
        self.screen.blit(self.text, self.text_rect)

    # Calcula los datos de la imagen
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

    # Dibuja los mejores arboles por cada generacion
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
        if self.flag==False:
            return

        if event.type != self.pygame.KEYDOWN:
            return

        if event.key != self.pygame.K_SPACE:
            return
        
        self.execute_state = (0, 255, 0)
        self.draw_circle_state()

        aux = self.set_area()

        self.trees_per_gen = {}
        self.totalArea=aux[0]
        self.img=aux[1]

        origin = [200, 400]

        population = generate_pob(100)
        amount_gens = 10

        data = pd.DataFrame([], columns = ['num_individuo', 'generacion', 'fitness'])

        for i in range(0, amount_gens):
            pob = test_pob(population, self.totalArea, self.img, origin)

            matrix = np.zeros((200, 200), dtype=int)
            self.tree_list.append(pob[0][1])
            result = []

            for k in range(len(pob)):
                row = pd.DataFrame([[k, i+1, pob[k][0]]], columns = ['num_individuo', 'generacion', 'fitness'])

                data.append(row)

                data = data.append(row)
                result.append(pob[0][1])
            
            # Guardamos las poblaciones por generacion - poblacion
            self.trees_per_gen[i] = result
            population = merge(result)

        self.genSlider.setData(np.arange(1, amount_gens+1))
        data.to_csv('resultados.csv', index=False)
        self.execute_state = (255, 0, 0)

    # E: Dibuja el circulo de estado de generacion
    def draw_circle_state(self):
        self.pygame.draw.circle(self.screen, self.execute_state, (20, 20), 20)
        self.pygame.display.update()