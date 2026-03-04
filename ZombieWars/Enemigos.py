import pygame

class Enemigo:
    def __init__(self, x, y, ancho=20, alto=20, sprite=None):
        # Rectángulo base
        self.forma = pygame.Rect(0, 0, ancho, alto)
        self.forma.center = (x, y)
        self.sprite = sprite  # opcional, para usar imagen luego

    def dibujar(self, pantalla):
        if self.sprite:
            # dibuja el sprite centrado
            rect_sprite = self.sprite.get_rect(center=self.forma.center)
            pantalla.blit(self.sprite, rect_sprite)
        else:
            # dibuja un rectángulo rojo como fallback
            pygame.draw.rect(pantalla, (255, 0, 0), self.forma)