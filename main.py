import pygame
import numpy as np
from view.home import Home

already = False

pygame.init()

home = Home(pygame)

home.start_game()