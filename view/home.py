from model.files import getImage
from view.window import Window

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

        self.game_loop()
