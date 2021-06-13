from abc import ABC, abstractmethod
import sys

class Window(ABC):
    # Desc: Inicializa las variables e inicia la ventana
    @abstractmethod
    def start_game(self):
        pass

    # Desc: Loop de la ventana. Solo debe encargarse de renderizar y eventos
    def game_loop(self):
        self.events.append(self.close)
        self.change_back()
        #self.append_render(self.change_back)
        while self.is_running:

            self.render()

            for event in self.pygame.event.get():
                for e in self.events:
                    e(event)

            self.pygame.display.update()
            self.main_clock.tick()

    def change_back(self):
        self.screen.fill(self.back_color)
        

    # Desc: Se encarga de renderizar
    def render(self):
        for ren in self.render_list:
            ren()

    # Desc: Permite agregar un evento al juego
    def append_event(self, event):
        self.events.append(event)

    # Desc: Permite agregar un evento de render externo
    # Rest: La funcion solo debe recibir el contexto de la clase y un Surface de Pygame
    def append_render(self, render):
        self.render_list.append(render)

    # E: Una referencia a un evento de Pygame
    # Desc: Cierra la ventan
    def close(self, event):
        if event.type == self.pygame.QUIT:
            self.pygame.quit()
            sys.exit()