import pygame
import random
from personaje import Personaje
from Enemigos import Enemigo
from constantes import * 

pygame.init()

# Ventana
pantalla = pygame.display.set_mode((ANCHO_VENTANA, ALTO_VENTANA))
pantalla_completa = False

# FPS
relog = pygame.time.Clock()

# Movimiento
mover_arriba = False
mover_abajo = False
mover_derecha = False
mover_izquierda = False
aumentar_velocidad = False
tiempo_ultimo_paso = 0

# Calcular grilla
def calcular_grilla(ancho, alto):
    cols = ancho // TAMANO_CELDA
    filas = alto // TAMANO_CELDA
    return filas, cols

# Generar mapa
def generar_mundo(filas, cols):
    mapa = [[0 for _ in range(cols)] for _ in range(filas)]
    for i in range(filas):
        for j in range(cols):
            if random.random() < 0.1:
                mapa[i][j] = 1
    mapa[1][1] = 0
    return mapa

# Cargar sprites
def cargar_sprites():
    asfalto = pygame.image.load("assets/images/suelo/AsfaltoBasico.png").convert_alpha()
    asfalto = pygame.transform.scale(asfalto, (TAMANO_CELDA, TAMANO_CELDA))
    
    obstaculos = [
        pygame.image.load("assets/images/obstaculos/carro.png").convert_alpha(),
        pygame.image.load("assets/images/obstaculos/hidrante.png").convert_alpha(),
        pygame.image.load("assets/images/obstaculos/Basurrero.png").convert_alpha()
    ]
    obstaculos = [pygame.transform.scale(s, (TAMANO_CELDA, TAMANO_CELDA)) for s in obstaculos]
    return asfalto, obstaculos

# Construir mapa de obstáculos
def construir_obstaculos(mapa, sprites):
    filas = len(mapa)
    cols = len(mapa[0]) if filas > 0 else 0
    obstaculo_mapa = [[None for _ in range(cols)] for _ in range(filas)]
    for i in range(filas):
        for j in range(cols):
            if mapa[i][j] == 1:
                obstaculo_mapa[i][j] = random.choice(sprites)
    return obstaculo_mapa

# Verificar colisión con enemigos
def hay_enemigo(fila, col, enemigos):
    for enemigo in enemigos:
        if enemigo["fila"] == fila and enemigo["col"] == col:
            return True
    return False

# Inicializar mundo
filas, cols = calcular_grilla(*pantalla.get_size())
mapa_grilla = generar_mundo(filas, cols)
asfalto, obstaculos = cargar_sprites()
obstaculo_mapa = construir_obstaculos(mapa_grilla, obstaculos)

# Jugador
jugador_fila = 1
jugador_col = 1
jugador = Personaje(0, 0)

# Enemigos
cantidad_enemigos = random.randint(MIN_ENEMIGOS, MAX_ENEMIGOS)
enemigos = []
distancia_minima = 5

for _ in range(cantidad_enemigos):
    for intento in range(1000):
        fila = random.randint(0, filas - 1)
        col = random.randint(0, cols - 1)
        if (mapa_grilla[fila][col] == 0 and 
            abs(fila - jugador_fila) >= distancia_minima and 
            abs(col - jugador_col) >= distancia_minima):
            enemigos.append({"obj": Enemigo(0, 0), "fila": fila, "col": col})
            break

# Reiniciar al cambiar tamaño
def reiniciar_sprites():
    global asfalto, obstaculos, obstaculo_mapa
    asfalto, obstaculos = cargar_sprites()
    obstaculo_mapa = construir_obstaculos(mapa_grilla, obstaculos)

# Loop principal
correr = True
while correr:
    relog.tick(FPS)

    # Obtener dimensiones actuales del mapa
    filas_mapa = len(mapa_grilla)
    cols_mapa = len(mapa_grilla[0]) if filas_mapa > 0 else 0

    # Dibujar mapa
    for i in range(filas_mapa):
        for j in range(cols_mapa):
            x = j * TAMANO_CELDA
            y = i * TAMANO_CELDA
            pantalla.blit(asfalto, (x, y))
            if mapa_grilla[i][j] == 1 and obstaculo_mapa[i][j]:
                pantalla.blit(obstaculo_mapa[i][j], (x, y))

    # Actualizar posición jugador
    jugador_x = jugador_col * TAMANO_CELDA + TAMANO_CELDA // 2
    jugador_y = jugador_fila * TAMANO_CELDA + TAMANO_CELDA // 2
    jugador.forma.center = (jugador_x, jugador_y)

    # Actualizar enemigos
    for enemigo in enemigos:
        enemigo_x = enemigo["col"] * TAMANO_CELDA + TAMANO_CELDA // 2
        enemigo_y = enemigo["fila"] * TAMANO_CELDA + TAMANO_CELDA // 2
        enemigo["obj"].forma.center = (enemigo_x, enemigo_y)

    # Movimiento
    tiempo_pasos = 100 if aumentar_velocidad else TIEMPO_ENTRE_PASOS
    tiempo_actual = pygame.time.get_ticks()
    
    if tiempo_actual - tiempo_ultimo_paso > tiempo_pasos:
        fila_nueva = jugador_fila
        col_nueva = jugador_col
        
        if mover_arriba:
            fila_nueva -= 1
            jugador.actualizar_direccion("arriba")
        elif mover_abajo:
            fila_nueva += 1
            jugador.actualizar_direccion("abajo")
        elif mover_izquierda:
            col_nueva -= 1
            jugador.actualizar_direccion("izquierda")
        elif mover_derecha:
            col_nueva += 1
            jugador.actualizar_direccion("derecha")

        # Validar movimiento
        if (0 <= fila_nueva < filas_mapa and 
            0 <= col_nueva < cols_mapa and 
            mapa_grilla[fila_nueva][col_nueva] == 0 and 
            not hay_enemigo(fila_nueva, col_nueva, enemigos)):
            jugador_fila = fila_nueva
            jugador_col = col_nueva
            tiempo_ultimo_paso = tiempo_actual

    # Actualizar estado del jugador
    moviendose = mover_arriba or mover_abajo or mover_izquierda or mover_derecha
    jugador.set_estado("run" if moviendose and aumentar_velocidad else "walk" if moviendose else "idle")
    
    # Dibujar
    jugador.dibujar(pantalla)
    for enemigo in enemigos:
        enemigo["obj"].dibujar(pantalla)

    # Eventos
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
                aumentar_velocidad = True
            if event.key == pygame.K_F11:
                if not pantalla_completa:
                    pantalla = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
                    pantalla_completa = True
                else:
                    pantalla = pygame.display.set_mode((ANCHO_VENTANA, ALTO_VENTANA))
                    pantalla_completa = False
                reiniciar_sprites()

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
                aumentar_velocidad = False

    pygame.display.update()

pygame.quit()