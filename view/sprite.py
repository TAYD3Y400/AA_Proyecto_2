class Sprite:

    # E: Referencia a imagen cargada por PyGame, cuatro enteros
    # S: N/A
    # D: Constructor de la clase
    def __init__(self, img, x, y, x_change, y_change, desc=""):
        self.x = x
        self.y = y

        self.x_change = x_change
        self.y_change = y_change

        self._img = img
        self.desc = desc

    def get_image(self):
        return self._img