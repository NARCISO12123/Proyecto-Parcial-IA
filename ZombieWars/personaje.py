import pygame

class Vida:

    def __init__(self, cantidad):

        self.cantidad = cantidad

    def perderVida(self):

        self.cantidad -= 1

        if self.cantidad <= 0:
            self.cantidad = 0
            return "GAME OVER"
    
    def recuperar(self):

        self.cantidad += 1
    
# personaje 
class Personaje:

    def __init__(self, x, y):

        self.forma = pygame.Rect(0, 0, 20, 20)
        self.forma.center = (x, y) 
        self.vida = Vida(5)

    #  funcion que dibuja el jugador
    def dibujar(self, pantalla):

        pygame.draw.rect(pantalla, (255,255,0), self.forma)

