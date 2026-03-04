import pygame
import os
import numpy as np
from constantes import TAMANO_CELDA

# Crop unificado para todos los sprites (elimina el negro de fondo)
# Abarca el personaje en todas las animaciones con un pequeño margen
CROP = (27, 54, 91, 128)  # (x1, y1, x2, y2) dentro de cada frame de 128x128


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


def hacer_negro_transparente(surface, umbral=20):
    """Convierte los pixels negros/muy oscuros en transparentes."""
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
    frames = []
    x1, y1, x2, y2 = CROP
    crop_w, crop_h = x2 - x1, y2 - y1

    for i in range(total):
        # Recortar frame del sheet
        frame_raw = sheet.subsurface((i * alto, 0, alto, alto)).copy()
        # Hacer negro transparente
        frame_clean = hacer_negro_transparente(frame_raw)
        # Recortar solo el personaje real
        frame_cropped = frame_clean.subsurface((x1, y1, crop_w, crop_h)).copy()
        # Escalar al tamaño de celda
        frame_scaled = pygame.transform.scale(frame_cropped, (TAMANO_CELDA, TAMANO_CELDA))
        frames.append(frame_scaled)

    return frames


class Personaje:

    def __init__(self, x, y):

        self.vida = Vida(5)

        base_path = os.path.dirname(os.path.dirname(__file__))
        carpeta = os.path.join(base_path, "assets", "images", "personaje")

        self.animaciones = {
            "idle":  cargar_frames(os.path.join(carpeta, "Idle.png"),   6),
            "idle2": cargar_frames(os.path.join(carpeta, "Idle_2.png"), 11),
            "walk":  cargar_frames(os.path.join(carpeta, "Walk.png"),   10),
            "run":   cargar_frames(os.path.join(carpeta, "Run.png"),    10),
        }

        self.estado = "idle"
        self.frame = 0
        self.tick = 0
        self.voltear = False
        self.direccion = "derecha"

        self.forma = pygame.Rect(0, 0, TAMANO_CELDA, TAMANO_CELDA)
        self.forma.center = (x, y)

    def set_estado(self, estado):
        if estado != self.estado:
            self.estado = estado
            self.frame = 0
            self.tick = 0

    def actualizar_direccion(self, direccion):
        self.direccion = direccion
        self.voltear = direccion in ("izquierda", "abajo")

    def dibujar(self, pantalla):
        self.tick += 1
        if self.tick % 8 == 0:
            self.frame = (self.frame + 1) % len(self.animaciones[self.estado])

        frame = self.animaciones[self.estado][self.frame]
        if self.voltear:
            frame = pygame.transform.flip(frame, True, False)

        pantalla.blit(frame, frame.get_rect(center=self.forma.center))