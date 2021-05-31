from model.files import getImage
from model.fractal import drawTree
from model.tree import Tree
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

        self.already = False
        
        self.click = False
        self.main_clock = pygame.time.Clock()

        self.screen = pygame.display.set_mode((600, 600))
        self.pygame.display.set_caption("Fractal Tree")

    # Override
    def start_game(self):
        self.is_running = True

        self.img = getImage("Example.png")

        self.append_render(self.draw_tree)

        self.game_loop()

    # D: Dibuja un arbol en pantalla
    def draw_tree(self):
        if self.already:
            return

        self.already = True

        tree_data = Tree()
        tree_data.x1 = 300
        tree_data.y1 = 600
        tree_data.angle = -90
        tree_data.depth = 9
        tree_data.fork_angle = 20
        tree_data.branch_angle = 45
        tree_data.base_len = 8
        tree_data.branch_base= 3
        tree_data.branches = 4

        origin = [200, 400]

        for x in range(len(self.img)):
            for y in range(len(self.img[0])):
                self.screen.set_at((x+origin[0], y + origin[1]), self.img[y][x]*255)

        print(np.sum(self.img[0][0]) == 4)

        rst = drawTree(tree_data, self.screen, self.img, origin)

        total = rst[0] + rst[1]

        area_out = 100*(rst[1] / total)
        area_in = 100*(rst[0] / total)

        print(rst)
        print("Porcentaje area dentro: ", area_in, "%")
        print("Porcentaje area afuera: ", area_out, "%")
