import os
import pygame
import random
from personaje import Personaje
from Enemigos import Enemigo
from constantes import *
from mapa import cargar_mapa_tmx, construir_grilla_colision, dibujar_mapa, cargar_colisiones, verificar_colision
from pantallas import pantalla_inicio, pantalla_game_over, menu_pausa, dibujar_mensaje_ronda, fuente_boton, COLOR_TITULO

pygame.init()
pygame.mixer.init()

# Ruta base del proyecto para cargar assets sin rutas hardcodeadas
BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Música de fondo en loop
pygame.mixer.music.load(os.path.join(BASE, "assets", "musica", "musica.mp3"))
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)

pantalla = pygame.display.set_mode((ANCHO_VENTANA, ALTO_VENTANA))
pygame.display.set_caption("Zombie Wars")
pantalla_completa = False
relog = pygame.time.Clock()

# Ruta al mapa del juego
RUTA_MAPA = os.path.join(BASE, "assets", "mapa", "mapa2.tmx")

# Cargamos el mapa antes de todo para poder calcular el tamaño del tile
mapa_tmx, filas, cols = cargar_mapa_tmx(RUTA_MAPA)

# Colores de las barras de vida
COLOR_VIDA_FONDO   = (80, 0, 0)
COLOR_VIDA_JUGADOR = (80, 220, 80)
COLOR_VIDA_ENEMIGO = (220, 60, 60)
COLOR_VIDA_BORDE   = (0, 0, 0)

# Colores HUD esquina
COLOR_HUD_FONDO = (15, 5, 25, 180)
COLOR_HUD_BARRA = (60, 200, 60)
COLOR_HUD_BAJA  = (220, 80, 40)
COLOR_HUD_VACIA = (60, 10, 10)
COLOR_HUD_BORDE = (200, 255, 100)
COLOR_HUD_TEXTO = (200, 255, 100)


try:
    fuente_hud_label = pygame.font.SysFont("impact", 16)
    fuente_hud_num   = pygame.font.SysFont("impact", 26)
except Exception:
    fuente_hud_label = pygame.font.Font(None, 16)
    fuente_hud_num   = pygame.font.Font(None, 26)


def dibujar_barra_vida(surface, cx, cy, vida_actual, vida_max, color_vida, ancho=30, alto=4):
    x = cx - ancho // 2
    y = cy
    pygame.draw.rect(surface, COLOR_VIDA_FONDO, (x, y, ancho, alto))
    relleno = int(ancho * max(vida_actual, 0) / vida_max)
    if relleno > 0:
        pygame.draw.rect(surface, color_vida, (x, y, relleno, alto))
    pygame.draw.rect(surface, COLOR_VIDA_BORDE, (x, y, ancho, alto), 1)


def dibujar_hud_vida(surface, vida_actual, vida_max):
    ancho_panel = 160
    alto_panel  = 48
    margen      = 12
    sw = surface.get_width()
    x_panel = sw - ancho_panel - margen
    y_panel = margen

    panel = pygame.Surface((ancho_panel, alto_panel), pygame.SRCALPHA)
    panel.fill(COLOR_HUD_FONDO)
    surface.blit(panel, (x_panel, y_panel))
    pygame.draw.rect(surface, COLOR_HUD_BORDE,
                     (x_panel, y_panel, ancho_panel, alto_panel), 2, border_radius=4)

    lbl = fuente_hud_label.render("HP", True, COLOR_HUD_TEXTO)
    surface.blit(lbl, (x_panel + 8, y_panel + 6))

    num_txt = fuente_hud_num.render(f"{max(vida_actual, 0)}", True, COLOR_HUD_TEXTO)
    surface.blit(num_txt, (x_panel + ancho_panel - num_txt.get_width() - 8, y_panel + 4))

    barra_x = x_panel + 8
    barra_y = y_panel + alto_panel - 16
    barra_w = ancho_panel - 16
    barra_h = 10
    pygame.draw.rect(surface, COLOR_HUD_VACIA, (barra_x, barra_y, barra_w, barra_h), border_radius=3)
    relleno = int(barra_w * max(vida_actual, 0) / vida_max)
    if relleno > 0:
        color_barra = COLOR_HUD_BAJA if vida_actual / vida_max < 0.30 else COLOR_HUD_BARRA
        pygame.draw.rect(surface, color_barra, (barra_x, barra_y, relleno, barra_h), border_radius=3)
    pygame.draw.rect(surface, COLOR_HUD_BORDE, (barra_x, barra_y, barra_w, barra_h), 1, border_radius=3)


# Mostramos el menú de inicio antes de entrar al juego
if not pantalla_inicio(pantalla, relog):
    pygame.quit()
    exit()


def hay_enemigo(fila, col, enemigos):
    return any(e["fila"] == fila and e["col"] == col for e in enemigos)


def animar(entidad, moviendose, corriendo=False, direccion=None):
    ahora = pygame.time.get_ticks()

    if getattr(entidad, "muriendo", False):
        entidad.actualizar_muerte()
        return

    if getattr(entidad, "disparando", False):
        velocidad_frame = 80
        if ahora - entidad.tiempo_ultimo_frame > velocidad_frame:
            entidad.frame_actual += 1
            entidad.tiempo_ultimo_frame = ahora
            if entidad.frame_actual >= len(entidad.animaciones["Shooting"]):
                entidad.disparando = False
                entidad.frame_actual = 0
                entidad.animacion_actual = "idle"
        frame = entidad.animaciones["Shooting"][min(entidad.frame_actual, len(entidad.animaciones["Shooting"]) - 1)]
        entidad.image = pygame.transform.flip(frame, entidad.voltear, False)
        return

    anim = "Running" if moviendose else "idle"
    velocidad_frame = 60 if corriendo else 100
    if anim != entidad.animacion_actual:
        entidad.animacion_actual = anim
        entidad.frame_actual = 0
        entidad.tiempo_ultimo_frame = ahora
    if ahora - entidad.tiempo_ultimo_frame > velocidad_frame:
        entidad.frame_actual = (entidad.frame_actual + 1) % len(entidad.animaciones[anim])
        entidad.tiempo_ultimo_frame = ahora

    if direccion == "izquierda":
        entidad.voltear = True
    elif direccion == "derecha":
        entidad.voltear = False
    frame = entidad.animaciones[entidad.animacion_actual][entidad.frame_actual]
    entidad.image = pygame.transform.flip(frame, entidad.voltear, False)


def dibujar_entidad(entidad, pantalla):
    pantalla.blit(entidad.image, entidad.forma)


def spawnar_enemigos():
    nuevos = []
    cantidad = random.randint(MIN_ENEMIGOS, MAX_ENEMIGOS) + ronda
    for _ in range(cantidad):
        for _ in range(1000):
            fila = random.randint(2, filas - 3)
            col  = random.randint(2, cols  - 3)
            if (mapa_grilla[fila][col] == 0 and
                abs(fila - jugador_fila) >= 5 and
                abs(col  - jugador_col)  >= 5 and
                not hay_enemigo(fila, col, nuevos)):
                nuevos.append({"obj": Enemigo(0, 0), "fila": fila, "col": col})
                break
    return nuevos


def reiniciar_partida():
    global jugador_fila, jugador_col, jugador, enemigos, mapa_grilla
    global ronda, mostrando_ronda, tiempo_mensaje_ronda, tiempo_ultimo_danio
    mapa_grilla = construir_grilla_colision(mapa_tmx, filas, cols)
    mapa_grilla[filas // 2][cols // 2] = 0
    jugador_fila, jugador_col = filas // 2, cols // 2
    jugador = Personaje(0, 0)
    ronda = 1
    mostrando_ronda = False
    tiempo_mensaje_ronda = 0
    tiempo_ultimo_danio  = 0
    enemigos = spawnar_enemigos()


escala_colision = TILE_SIZE / mapa_tmx.tilewidth
colisiones = cargar_colisiones(mapa_tmx, escala_colision)

ronda = 1
mostrando_ronda = False
tiempo_mensaje_ronda = 0
tiempo_ultimo_danio  = 0

reiniciar_partida()

# Variables de movimiento del jugador
mover_arriba      = False
mover_abajo       = False
mover_izquierda   = False
mover_derecha     = False
aumentar_velocidad = False
tiempo_ultimo_paso = 0

# ── Bucle principal
correr = True
while correr:
    relog.tick(FPS)

    pantalla.fill((25, 8, 40))

    ancho_actual, alto_actual = pantalla.get_size()
    offset_x = (ancho_actual - cols * TILE_SIZE) // 2
    offset_y = (alto_actual  - filas * TILE_SIZE) // 2

    dibujar_mapa(pantalla, mapa_tmx, TILE_SIZE, offset_x, offset_y)

    # Posicionamos al jugador en su celda del mapa
    jugador.forma.center = (
        offset_x + jugador_col  * TILE_SIZE + TILE_SIZE // 2,
        offset_y + jugador_fila * TILE_SIZE + TILE_SIZE // 2,
    )

    # Posicionamos a cada enemigo en su celda
    for enemigo in enemigos:
        enemigo["obj"].forma.center = (
            offset_x + enemigo["col"]  * TILE_SIZE + TILE_SIZE // 2,
            offset_y + enemigo["fila"] * TILE_SIZE + TILE_SIZE // 2,
        )

    tiempo_pasos  = 100 if aumentar_velocidad else TIEMPO_ENTRE_PASOS
    tiempo_actual = pygame.time.get_ticks()

    # Movimiento del jugador (bloqueado si está muriendo o muerto)
    if not jugador.muriendo and not jugador.muerto:
        if tiempo_actual - tiempo_ultimo_paso > tiempo_pasos:
            fila_nueva = jugador_fila
            col_nueva  = jugador_col

            if mover_arriba:
                fila_nueva -= 1
            elif mover_abajo:
                fila_nueva += 1
            elif mover_izquierda:
                col_nueva -= 1
            elif mover_derecha:
                col_nueva += 1

            rect_jugador = pygame.Rect(
                offset_x + col_nueva  * TILE_SIZE,
                offset_y + fila_nueva * TILE_SIZE,
                TILE_SIZE, TILE_SIZE
            )
            rects_colision_offset = [
                pygame.Rect(r.x + offset_x, r.y + offset_y, r.width, r.height)
                for r in colisiones
            ]

            if (0 <= fila_nueva < filas and
                0 <= col_nueva  < cols  and
                not hay_enemigo(fila_nueva, col_nueva, enemigos) and
                not verificar_colision(rect_jugador, 0, 0, rects_colision_offset, ancho_actual, alto_actual)):
                jugador_fila, jugador_col = fila_nueva, col_nueva
                tiempo_ultimo_paso = tiempo_actual

    moviendose = mover_arriba or mover_abajo or mover_izquierda or mover_derecha
    direccion  = "izquierda" if mover_izquierda else "derecha" if mover_derecha else None
    animar(jugador, moviendose, aumentar_velocidad, direccion)
    dibujar_entidad(jugador, pantalla)

    # Barra pequeña encima del sprite del jugador
    dibujar_barra_vida(
        pantalla,
        jugador.forma.centerx,
        jugador.forma.top - 8,
        jugador.vida,
        VIDA_MAX_JUGADOR,
        COLOR_VIDA_JUGADOR,
        ancho=32, alto=5
    )

    # HUD grande de vida en esquina superior derecha
    dibujar_hud_vida(pantalla, jugador.vida, VIDA_MAX_JUGADOR)

    # Balas
    if not jugador.muriendo and not jugador.muerto:
        impactados = jugador.actualizar_balas(mapa_grilla, enemigos)
        for e in impactados:
            e["obj"].recibir_danio(DANIO_BALA)
        for bala in jugador.balas:
            bala.dibujar(pantalla)

    # Actualización de enemigos con A* y árbol de comportamiento
    for enemigo in enemigos[:]:
        obj = enemigo["obj"]

        nueva_fila, nueva_col = obj.actualizar(
            enemigo["fila"],
            enemigo["col"],
            jugador_fila,
            jugador_col,
            mapa_grilla,
            enemigos,
        )
        enemigo["fila"] = nueva_fila
        enemigo["col"]  = nueva_col

        # Eliminar enemigos cuya animación de muerte terminó
        if not obj.vivo:
            enemigos.remove(enemigo)
            continue

        dibujar_entidad(obj, pantalla)

        # Barra de vida del enemigo encima de su sprite
        dibujar_barra_vida(
            pantalla,
            obj.forma.centerx,
            obj.forma.top - 8,
            obj.vida,
            VIDA_MAX_ENEMIGO,
            COLOR_VIDA_ENEMIGO,
            ancho=28, alto=4
        )

        # Daño por proximidad: usamos distancia en píxeles entre sprites
        if not obj.muriendo and not jugador.muriendo and not jugador.muerto:
            dx = obj.forma.centerx - jugador.forma.centerx
            dy = obj.forma.centery - jugador.forma.centery
            dist_px = (dx * dx + dy * dy) ** 0.5
            
            if (dist_px <= DIST_DANIO_PX and
                    tiempo_actual - tiempo_ultimo_danio > INTERVALO_DANIO):
                jugador.recibir_danio(DANIO_CONTACTO)
                tiempo_ultimo_danio = tiempo_actual

    # Cuando la animación de muerte del jugador termina → Game Over
    if jugador.muerto:
        seguir = pantalla_game_over(pantalla, relog)
        if seguir:
            reiniciar_partida()
        else:
            correr = False
        continue

    # Si no quedan enemigos, subimos la ronda
    if not enemigos and not mostrando_ronda:
        ronda += 1
        mostrando_ronda = True
        tiempo_mensaje_ronda = pygame.time.get_ticks()

        # Cada 5 rondas la vida máxima y actual del jugador suben 10
        if ronda % 5 == 0:
            jugador.VIDA_MAX += 20
            jugador.vida     += 10

    # Mostramos el mensaje de nueva ronda por 2 segundos
    if mostrando_ronda:
        dibujar_mensaje_ronda(pantalla, ronda)
        if pygame.time.get_ticks() - tiempo_mensaje_ronda > 2000:
            mostrando_ronda = False
            enemigos = spawnar_enemigos()

    # Número de ronda actual en la esquina superior izquierda
    txt_ronda = fuente_boton.render(f"Ronda: {ronda}", True, COLOR_TITULO)
    pantalla.blit(txt_ronda, (10, 10))

    # Eventos del juego
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            correr = False

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mx, my = pygame.mouse.get_pos()
            jugador.disparar(mx, my)

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                accion = menu_pausa(pantalla, relog)
                if accion == "salir":
                    correr = False
                elif accion == "reiniciar":
                    reiniciar_partida()

            if event.key == pygame.K_w:
                mover_arriba = True
            
            if event.key == pygame.K_s:
                mover_abajo = True
            
            if event.key == pygame.K_a:
                mover_izquierda = True
            
            if event.key == pygame.K_d:
                mover_derecha = True
            
            if event.key == pygame.K_LSHIFT:
                aumentar_velocidad = True

            if event.key == pygame.K_HOME:
                
                if not pantalla_completa:
                    pantalla = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
                    pantalla_completa = True
                
                else:
                    pantalla = pygame.display.set_mode((ANCHO_VENTANA, ALTO_VENTANA))
                    pantalla_completa = False

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_w:
                mover_arriba = False
            
            if event.key == pygame.K_s:
                mover_abajo = False
            
            if event.key == pygame.K_a:
                mover_izquierda = False
            
            if event.key == pygame.K_d:
                mover_derecha = False
            
            if event.key == pygame.K_LSHIFT:
                aumentar_velocidad = False

    pygame.display.update()

pygame.quit()