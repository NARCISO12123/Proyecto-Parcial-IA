import pygame
import os
from constantes import TAMANO_CELDA

CROP_ENEMIGO = (27, 54, 91, 128)

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

def cargar_frames_enemigo(ruta):
    """Carga todos los frames del spritesheet con recorte"""
    sheet = pygame.image.load(ruta).convert_alpha()
    
    alto = sheet.get_height()
    ancho_total = sheet.get_width()
    total_frames = ancho_total // alto
    
    x1, y1, x2, y2 = CROP_ENEMIGO
    crop_w, crop_h = x2 - x1, y2 - y1
    
    frames = []
    for i in range(total_frames):
        frame = sheet.subsurface((i * alto, 0, alto, alto)).copy()
        frame = hacer_negro_transparente(frame)
        frame_cropped = frame.subsurface((x1, y1, crop_w, crop_h)).copy()
        frame = pygame.transform.scale(frame_cropped, (TAMANO_CELDA, TAMANO_CELDA))
        frames.append(frame)
    
    return frames

class Enemigo:
    def __init__(self, x, y):
        base_path = os.path.dirname(os.path.dirname(__file__))
        ruta_sprite = os.path.join(base_path, "assets", "images", "enemigos", "parado.png")
        
        self.frames = cargar_frames_enemigo(ruta_sprite)
        self.frame_actual = 0
        self.tick = 0
        
        self.forma = pygame.Rect(0, 0, TAMANO_CELDA, TAMANO_CELDA)
        self.forma.center = (x, y)

    def dibujar(self, pantalla):
        self.tick += 1
        if self.tick % 8 == 0:
            self.frame_actual = (self.frame_actual + 1) % len(self.frames)
        
        sprite = self.frames[self.frame_actual]
        rect_sprite = sprite.get_rect(center=self.forma.center)
        pantalla.blit(sprite, rect_sprite)