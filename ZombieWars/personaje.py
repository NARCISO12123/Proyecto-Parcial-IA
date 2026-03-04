import pygame
import os
import numpy as np
from constantes import TAMANO_CELDA

CROP = (27, 54, 91, 128)


def hacer_negro_transparente(surface, umbral=20):
    """Convierte pixels negros/muy oscuros en transparentes."""
    arr = pygame.surfarray.pixels3d(surface).copy()
    alpha = pygame.surfarray.pixels_alpha(surface).copy()
    es_negro = (arr[:,:,0] < umbral) & (arr[:,:,1] < umbral) & (arr[:,:,2] < umbral)
    alpha[es_negro] = 0
    result = pygame.Surface(surface.get_size(), pygame.SRCALPHA)
    pygame.surfarray.blit_array(result, arr)
    pygame.surfarray.pixels_alpha(result)[:] = alpha
    return result


def cargar_frames(ruta, total):
    sheet = pygame.image.load(ruta).convert_alpha()
    alto = sheet.get_height()
    x1, y1, x2, y2 = CROP
    frames = []

    for i in range(total):
        frame = sheet.subsurface((i * alto, 0, alto, alto)).copy()
        frame = hacer_negro_transparente(frame)
        frame = frame.subsurface((x1, y1, x2-x1, y2-y1)).copy()  # ← Calculado directamente
        frame = pygame.transform.scale(frame, (TAMANO_CELDA, TAMANO_CELDA))
        frames.append(frame)

    return frames

class Personaje:

    def __init__(self, x, y):
        self.vida = 5
        
        carpeta = os.path.join(os.path.dirname(os.path.dirname(__file__)), 
                               "assets", "images", "personaje")

        self.animaciones = {
            "idle":  cargar_frames(os.path.join(carpeta, "Idle.png"), 6),
            "idle2": cargar_frames(os.path.join(carpeta, "Idle_2.png"), 11),
            "walk":  cargar_frames(os.path.join(carpeta, "Walk.png"), 10),
            "run":   cargar_frames(os.path.join(carpeta, "Run.png"), 10),
        }

        self.estado = "idle"
        self.frame = 0
        self.tick = 0
        self.voltear = False

        self.forma = pygame.Rect(0, 0, TAMANO_CELDA, TAMANO_CELDA)
        self.forma.center = (x, y)

    def perder_vida(self):
        self.vida = max(0, self.vida - 1)
        return self.vida == 0

    def recuperar_vida(self):
        self.vida += 1

    def set_estado(self, estado):
        if estado != self.estado:
            self.estado = estado
            self.frame = 0
            self.tick = 0

    def actualizar_direccion(self, direccion):
        self.voltear = direccion in ("izquierda", "abajo")

    def dibujar(self, pantalla):
        self.tick += 1
        if self.tick % 8 == 0:
            self.frame = (self.frame + 1) % len(self.animaciones[self.estado])

        frame = self.animaciones[self.estado][self.frame]
        if self.voltear:
            frame = pygame.transform.flip(frame, True, False)

        pantalla.blit(frame, frame.get_rect(center=self.forma.center))