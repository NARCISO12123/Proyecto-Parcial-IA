# Nombre:  Narciso Beras 
# Matrícula:  24-EISN-2-026


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
MIN_ENEMIGOS = 1
MAX_ENEMIGOS = 4

# FPS
FPS = 60

ESCALA_JUGADOR = 0.1
ESCALA_ENEMIGO = 0.1

# Tiempo entre pasos del jugador (milisegundos)
TIEMPO_ENTRE_PASOS = 200

# Tamaño de cada tile en píxeles
TILE_SIZE = 22

# Vida y daño 
VIDA_MAX_JUGADOR = 100
VIDA_MAX_ENEMIGO = 100

DANIO_BALA      = 20 
DANIO_CONTACTO  = 10    
INTERVALO_DANIO = 800   

DIST_DANIO_PX   = TILE_SIZE * 1.5  