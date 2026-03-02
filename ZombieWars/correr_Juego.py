import pygame
import random
from personaje import Personaje
from Enemigos import Enemigo
from constantes import * 
pygame.init()

# Color de fondo de la ventana
color_fondo = COLOR_FONDO

# Crear ventana principal
pantalla = pygame.display.set_mode((ANCHO_VENTANA, ALTO_VENTANA), pygame.RESIZABLE)
pantallaCompleta = False

# Configuración de FPS
fps = FPS
relog = pygame.time.Clock()

# Estados de movimiento del jugador
mover_arriba = False
mover_abajo = False
mover_derecha = False
mover_izquierda = False

# Control de velocidad por pasos
tiempo_ultimo_paso = 0
aumentarVelocidad = False

# Cargar sprite de asfalto
asfalto_sprite = pygame.image.load("assets/images/suelo/AsfaltoBasico.png").convert_alpha()

# Cargar los sprites de obstáculos 
obstaculo_sprites = [
    pygame.image.load("assets/images/obstaculos/carro.png").convert_alpha(),
    pygame.image.load("assets/images/obstaculos/hidrante.png").convert_alpha(),
    pygame.image.load("assets/images/obstaculos/Basurrero.png").convert_alpha()
]

# Generar mapa con muros aleatorios
def generar_mundo(n):
    mapa = [[0 for _ in range(n)] for _ in range(n)]
    for i in range(n):
        for j in range(n):
            if random.random() < 0.1:
                mapa[i][j] = 1
    return mapa

# Crear mapa
tamano_mapa = TAMANO_MAPA
mapa_grilla = generar_mundo(tamano_mapa)

# Mapa de sprites para obstáculos (fijo por partida)
obstaculo_mapa = [[None for _ in range(tamano_mapa)] for _ in range(tamano_mapa)]
for i in range(tamano_mapa):
    for j in range(tamano_mapa):
        if mapa_grilla[i][j] == 1:
            obstaculo_mapa[i][j] = random.choice(obstaculo_sprites)

# Posición inicial del jugador
jugador_fila = 1
jugador_col = 1

# Crear objeto jugador
Jugador = Personaje(0, 0)

# Generar enemigos lejos del jugador
cantidad_enemigos = random.randint(MIN_ENEMIGOS, MAX_ENEMIGOS)
enemigos = []

distancia_minima = 10
for _ in range(cantidad_enemigos):
    while True:
        fila = random.randint(0, tamano_mapa - 1)
        col = random.randint(0, tamano_mapa - 1)

        if (mapa_grilla[fila][col] == 0 and
            abs(fila - jugador_fila) >= distancia_minima and
            abs(col - jugador_col) >= distancia_minima):

            enemigo = Enemigo(0, 0)
            enemigos.append({
                "obj": enemigo,
                "fila": fila,
                "col": col
            })
            break

# Bucle principal
correr = True
while correr:
    relog.tick(fps)
    pantalla.fill(color_fondo)

    # Ajustar tamaño dinámico de la grilla
    ancho, alto = pantalla.get_size()
    cell_size = min(ancho // tamano_mapa, alto // tamano_mapa)
    offset_x = (ancho - (cell_size * tamano_mapa)) // 2
    offset_y = (alto - (cell_size * tamano_mapa)) // 2

    # Convertir posición del jugador a coordenadas de pantalla
    jugador_x = offset_x + jugador_col * cell_size + cell_size // 2
    jugador_y = offset_y + jugador_fila * cell_size + cell_size // 2
    Jugador.forma.center = (jugador_x, jugador_y)

    # Actualizar posición visual de los enemigos
    for enemigo in enemigos:
        enemigo_x = offset_x + enemigo["col"] * cell_size + cell_size // 2
        enemigo_y = offset_y + enemigo["fila"] * cell_size + cell_size // 2
        enemigo["obj"].forma.center = (enemigo_x, enemigo_y)

    # Dibujar mapa con sprites
    for i in range(tamano_mapa):
        for j in range(tamano_mapa):
            rect_celda = pygame.Rect(
                offset_x + j * cell_size,
                offset_y + i * cell_size,
                cell_size, cell_size
            )

            if mapa_grilla[i][j] == 0:  # Suelo
                sprite_escalado = pygame.transform.scale(asfalto_sprite, (cell_size, cell_size))
                pantalla.blit(sprite_escalado, rect_celda.topleft)
            else:  # Obstáculo
                sprite_obst = obstaculo_mapa[i][j]
                sprite_escalado = pygame.transform.scale(sprite_obst, (cell_size, cell_size))
                pantalla.blit(sprite_escalado, rect_celda.topleft)

    # Ajustar tiempo entre pasos según Shift
    if aumentarVelocidad:
        tiempo_pasos = 100  # más rápido
    else:
        tiempo_pasos = TIEMPO_ENTRE_PASOS  # normal

    # Movimiento del jugador por pasos
    tiempo_actual = pygame.time.get_ticks()
    if tiempo_actual - tiempo_ultimo_paso > tiempo_pasos:
        fila_nueva = jugador_fila
        col_nueva = jugador_col

        if mover_arriba:
            fila_nueva -= 1
        elif mover_abajo:
            fila_nueva += 1
        elif mover_izquierda:
            col_nueva -= 1
        elif mover_derecha:
            col_nueva += 1

        # Validar límites y muros
        if (0 <= fila_nueva < tamano_mapa and
            0 <= col_nueva < tamano_mapa and
            mapa_grilla[fila_nueva][col_nueva] == 0):

            jugador_fila = fila_nueva
            jugador_col = col_nueva
            tiempo_ultimo_paso = tiempo_actual

    # Dibujar jugador
    Jugador.dibujar(pantalla)

    # Dibujar enemigos
    for enemigo in enemigos:
        enemigo["obj"].dibujar(pantalla)

    # Manejo de eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            correr = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                correr = False
            if event.key == pygame.K_a:
                mover_izquierda = True
            if event.key == pygame.K_s:
                mover_abajo = True
            if event.key == pygame.K_d:
                mover_derecha = True
            if event.key == pygame.K_w:
                mover_arriba = True
            if event.key == pygame.K_LSHIFT:
                aumentarVelocidad = True

            # Alternar pantalla completa
            if event.key == pygame.K_F11:
                if not pantallaCompleta:
                    pantalla = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
                    pantallaCompleta = True
                else:
                    pantalla = pygame.display.set_mode((ANCHO_VENTANA, ALTO_VENTANA), pygame.RESIZABLE)
                    pantallaCompleta = False

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                mover_izquierda = False
            if event.key == pygame.K_s:
                mover_abajo = False
            if event.key == pygame.K_d:
                mover_derecha = False
            if event.key == pygame.K_w:
                mover_arriba = False
            if event.key == pygame.K_LSHIFT:
                aumentarVelocidad = False

    pygame.display.update()

pygame.quit()