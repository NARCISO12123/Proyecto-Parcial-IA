import pygame
import random
from personaje import Personaje
from Enemigos import Enemigo
from constantes import * 
pygame.init()

# Crear ventana principal
pantalla = pygame.display.set_mode((ANCHO_VENTANA, ALTO_VENTANA))
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

# Tamaño fijo de celda
cell_size = TAMANO_CELDA

# Cargar sprite de asfalto
asfalto_sprite = pygame.image.load("assets/images/suelo/AsfaltoBasico.png").convert_alpha()
asfalto_scaled = pygame.transform.scale(asfalto_sprite, (cell_size, cell_size))

# Cargar los sprites de obstáculos 
obstaculo_sprites = [
    pygame.image.load("assets/images/obstaculos/carro.png").convert_alpha(),
    pygame.image.load("assets/images/obstaculos/hidrante.png").convert_alpha(),
    pygame.image.load("assets/images/obstaculos/Basurrero.png").convert_alpha()
]
obstaculo_sprites_scaled = [
    pygame.transform.scale(s, (cell_size, cell_size)) for s in obstaculo_sprites
]

# Calcular tamaño del mapa según la ventana (cubre toda la pantalla)
def calcular_tamano_mapa(ancho, alto, cell):
    cols = (ancho + cell - 1) // cell
    filas = (alto + cell - 1) // cell
    return filas, cols

# Generar mapa con muros aleatorios
def generar_mundo(filas, cols):
    mapa = [[0 for _ in range(cols)] for _ in range(filas)]
    for i in range(filas):
        for j in range(cols):
            if random.random() < 0.1:
                mapa[i][j] = 1
    # Asegurar posición inicial libre
    mapa[1][1] = 0
    return mapa

ancho_inicial, alto_inicial = pantalla.get_size()
tamano_filas, tamano_cols = calcular_tamano_mapa(ancho_inicial, alto_inicial, cell_size)

mapa_grilla = generar_mundo(tamano_filas, tamano_cols)

# Mapa de sprites para obstáculos
obstaculo_mapa = [[None for _ in range(tamano_cols)] for _ in range(tamano_filas)]
for i in range(tamano_filas):
    for j in range(tamano_cols):
        if mapa_grilla[i][j] == 1:
            obstaculo_mapa[i][j] = random.choice(obstaculo_sprites_scaled)

# Posición inicial del jugador
jugador_fila = 1
jugador_col = 1

# Crear objeto jugador
Jugador = Personaje(0, 0)

# Generar enemigos y obstaculos lejos del jugador
cantidad_enemigos = random.randint(MIN_ENEMIGOS, MAX_ENEMIGOS)
enemigos = []

distancia_minima = 10
for _ in range(cantidad_enemigos):
    intentos = 0
    while intentos < 1000:
        fila = random.randint(0, tamano_filas - 1)
        col = random.randint(0, tamano_cols - 1)

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
        intentos += 1

# Bucle principal
correr = True
while correr:
    relog.tick(fps)

    ancho, alto = pantalla.get_size()

    # Dibujar mapa 
    for i in range(tamano_filas):
        for j in range(tamano_cols):
            x = j * cell_size
            y = i * cell_size
            if mapa_grilla[i][j] == 0:
                pantalla.blit(asfalto_scaled, (x, y))
            else:
                pantalla.blit(obstaculo_mapa[i][j], (x, y))

    # Convertir posición del jugador a coordenadas de pantalla
    jugador_x = jugador_col * cell_size + cell_size // 2
    jugador_y = jugador_fila * cell_size + cell_size // 2
    Jugador.forma.center = (jugador_x, jugador_y)

    # Actualizar posición visual de los enemigos
    for enemigo in enemigos:
        enemigo_x = enemigo["col"] * cell_size + cell_size // 2
        enemigo_y = enemigo["fila"] * cell_size + cell_size // 2
        enemigo["obj"].forma.center = (enemigo_x, enemigo_y)

    # Ajustar tiempo entre pasos según Shift
    tiempo_pasos = 100 if aumentarVelocidad else TIEMPO_ENTRE_PASOS

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

        if (0 <= fila_nueva < tamano_filas and
            0 <= col_nueva < tamano_cols and
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

            if event.key == pygame.K_F11:
                if not pantallaCompleta:
                    pantalla = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
                    pantallaCompleta = True
                else:
                    pantalla = pygame.display.set_mode((ANCHO_VENTANA, ALTO_VENTANA))
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