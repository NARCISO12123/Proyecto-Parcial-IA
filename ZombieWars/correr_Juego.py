import pygame
import personaje
import Enemigos
import random
from personaje import Personaje
from Enemigos import Enemigo

pygame.init()

# Color de fondo
color_fondo = (0, 0, 20)

# Ventana
pantalla = pygame.display.set_mode((1280, 720), pygame.RESIZABLE)
pantallaCompleta = False

fps = 60
relog = pygame.time.Clock()

# Movimiento
mover_arriba = False
mover_abajo = False
mover_derecha = False 
mover_izquierda = False

# Control de velocidad por casillas
tiempo_entre_pasos = 100
ultimo_paso = 0


def generar_mundo(n, pos_jugador):
    mapa = [[0 for _ in range(n)] for _ in range(n)]

    destino = [random.randint(1, n-1), random.randint(1, n-1)]
    mapa[destino[0]][destino[1]] = "E"

    for i in range(n):
        for j in range(n):
            if (i, j) == pos_jugador:
                continue
            if (i, j) == tuple(destino):
                continue
            if random.random() < 0.1:
                mapa[i][j] = 1

    # Evita que el personaje quede atrapado al inicio
    jf, jc = pos_jugador
    mapa[jf][jc] = 0

    for dx, dy in [(-1,0),(1,0),(0,-1),(0,1)]:
        nf = jf + dx
        nc = jc + dy
        if 0 <= nf < n and 0 <= nc < n:
            mapa[nf][nc] = 0

    return mapa, destino


def generar_posicion_enemigo(mapa, n, pos_jugador, distancia_minima):

    while True:
        # Genera una posición aleatoria dentro del mapa
        fila = random.randint(0, n-1)
        col = random.randint(0, n-1)

        if mapa[fila][col] != 0:
            continue

        # Calcula la distancia respecto al jugador
        distancia = abs(fila - pos_jugador[0]) + abs(col - pos_jugador[1])

        # Asegura que no aparezca demasiado cerca del personaje
        if distancia >= distancia_minima:
            return fila, col


tamano_mapa = 25     

# Posición en celdas
jugador_fila = 1
jugador_col = 1

mapa_grilla, posicion_salida = generar_mundo(
    tamano_mapa,
    (jugador_fila, jugador_col)
)

zombie_fila, zombie_col = generar_posicion_enemigo(
    mapa_grilla,
    tamano_mapa,
    (jugador_fila, jugador_col),
    6
)

print(f"Mapa generado: {tamano_mapa}x{tamano_mapa} | Salida en {posicion_salida}")

Jugador = Personaje(0, 0)
Zombie = Enemigo(0, 0)

correr = True

while correr:

    relog.tick(fps)
    pantalla.fill(color_fondo)

    ancho, alto = pantalla.get_size()
    cell_size = min(ancho // tamano_mapa, alto // tamano_mapa)
    offset_x = (ancho - (cell_size * tamano_mapa)) // 2
    offset_y = (alto - (cell_size * tamano_mapa)) // 2

    # Posición visual del jugador
    jugador_x = offset_x + jugador_col * cell_size + cell_size // 2
    jugador_y = offset_y + jugador_fila * cell_size + cell_size // 2
    Jugador.forma.center = (jugador_x, jugador_y)

    # Posición visual del zombie
    zombie_x = offset_x + zombie_col * cell_size + cell_size // 2
    zombie_y = offset_y + zombie_fila * cell_size + cell_size // 2
    Zombie.forma.center = (zombie_x, zombie_y)

    # Dibujar mapa
    for i in range(tamano_mapa):
        for j in range(tamano_mapa):

            rect_celda = pygame.Rect(
                offset_x + j * cell_size,
                offset_y + i * cell_size,
                cell_size, cell_size
            )

            if mapa_grilla[i][j] == 1:
                pygame.draw.rect(pantalla, (50, 50, 50), rect_celda)
            elif mapa_grilla[i][j] == "E":
                pygame.draw.rect(pantalla, (0, 255, 0), rect_celda)
                pygame.draw.rect(pantalla, (255, 255, 255), rect_celda, 2)
            else:
                pygame.draw.rect(pantalla, (80, 80, 80), rect_celda)
                pygame.draw.rect(pantalla, (100, 100, 100), rect_celda, 1)

    # Movimiento controlado por tiempo
    tiempo_actual = pygame.time.get_ticks()

    if tiempo_actual - ultimo_paso > tiempo_entre_pasos:

        fila_nueva = jugador_fila
        col_nueva = jugador_col

        if mover_arriba:
            fila_nueva -= 1
        if mover_abajo:
            fila_nueva += 1
        if mover_izquierda:
            col_nueva -= 1
        if mover_derecha:
            col_nueva += 1

        if (0 <= fila_nueva < tamano_mapa and
            0 <= col_nueva < tamano_mapa and
            mapa_grilla[fila_nueva][col_nueva] == 0):

            jugador_fila = fila_nueva
            jugador_col = col_nueva
            ultimo_paso = tiempo_actual

    # Dibujar personajes
    Jugador.dibujar(pantalla)
    Zombie.dibujar(pantalla)

    # Eventos
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            correr = False
        
        # eventos para presionar boton 
        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_a:
                mover_izquierda = True
            if event.key == pygame.K_s:
                mover_abajo = True
            if event.key == pygame.K_d:
                mover_derecha = True
            if event.key == pygame.K_w:
                mover_arriba = True

            # pantalla completa
            if event.key == pygame.K_x:
               
                if pantallaCompleta == False:
                    pantallaCompleta = True
                    pantalla = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
                else:
                    pantalla = pygame.display.set_mode((1280, 720), pygame.RESIZABLE)
                    pantallaCompleta = False
        
        # evento para soltar
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                mover_izquierda = False
            if event.key == pygame.K_s:
                mover_abajo = False
            if event.key == pygame.K_d:
                mover_derecha = False
            if event.key == pygame.K_w:
                mover_arriba = False

    pygame.display.update()

pygame.quit()