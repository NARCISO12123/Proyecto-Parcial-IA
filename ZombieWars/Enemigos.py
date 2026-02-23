import pygame
import personaje
from personaje import Vida

class Enemigo:

    def __init__(self, x , y):
        
        self.forma = pygame.Rect(0, 0, 20, 20)
        self.forma.center = (x, y) 
        self.vida = Vida(2)

    def dibujar(self, pantalla):

        pygame.draw.rect(pantalla, (255, 0, 0), self.forma)

