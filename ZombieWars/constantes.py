import pygame
pygame.init()
info = pygame.display.Info()
ANCHO_VENTANA = info.current_w
ALTO_VENTANA  = info.current_h

# Color de fondo
COLOR_FONDO = (0, 0, 0)

# Tamaño del mapa 
TAMANO_MAPA = 20
TAMANO_CELDA = 32

# Enemigos
MIN_ENEMIGOS = 5
MAX_ENEMIGOS = 12

# FPS
FPS = 60

ESCALA_JUGADOR = 0.1
ESCALA_ENEMIGO = 0.1

# Tiempo entre pasos del jugador (milisegundos)
TIEMPO_ENTRE_PASOS = 200