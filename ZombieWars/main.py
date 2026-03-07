import os
import pygame
import random
from personaje import Personaje
from Enemigos import Enemigo
from constantes import *
from mapa import cargar_mapa_tmx, construir_grilla_colision, dibujar_mapa, cargar_colisiones, verificar_colision

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

# Tamaño de cada tile en píxeles
TILE_SIZE = 22

# Colores del menú
COLOR_FONDO       = (25, 8, 40)
COLOR_TITULO      = (200, 255, 100)
COLOR_BTN         = (200, 255, 100)
COLOR_BTN_HOV     = (220, 255, 140)
COLOR_BTN_SAL     = (180, 60, 60)
COLOR_BTN_SAL_HOV = (220, 90, 90)
COLOR_TEXTO       = (25, 8, 40)

# Fuentes para el menú y los mensajes de ronda
try:
    fuente_titulo  = pygame.font.SysFont("impact", 80)
    fuente_boton   = pygame.font.SysFont("impact", 32)
    fuente_ronda   = pygame.font.SysFont("impact", 60)
except Exception:
    fuente_titulo  = pygame.font.Font(None, 80)
    fuente_boton   = pygame.font.Font(None, 32)
    fuente_ronda   = pygame.font.Font(None, 60)


def dibujar_boton(surface, texto, rect, color_base, color_hover, color_txt, fuente):
    hover = rect.collidepoint(pygame.mouse.get_pos())
    pygame.draw.rect(surface, color_hover if hover else color_base, rect, border_radius=6)
    txt_surf = fuente.render(texto, True, color_txt)
    surface.blit(txt_surf, txt_surf.get_rect(center=rect.center))
    return hover

def pantalla_inicio():
    ancho, alto = pantalla.get_size()
    btn_w, btn_h = 260, 55
    cx = ancho // 2
    btn_jugar = pygame.Rect(cx - btn_w // 2, alto // 2 + 20,  btn_w, btn_h)
    btn_salir = pygame.Rect(cx - btn_w // 2, alto // 2 + 100, btn_w, btn_h)

    # Bucle del menú de inicio
    while True:
        relog.tick(60)
        pantalla.fill(COLOR_FONDO)
        tit = fuente_titulo.render("ZOMBIE WARS", True, COLOR_TITULO)
        pantalla.blit(tit, tit.get_rect(center=(cx, alto // 2 - 80)))
        hover_jugar = dibujar_boton(pantalla, "INICIAR JUEGO", btn_jugar, COLOR_BTN,     COLOR_BTN_HOV,     COLOR_TEXTO,     fuente_boton)
        hover_salir = dibujar_boton(pantalla, "SALIR",         btn_salir, COLOR_BTN_SAL, COLOR_BTN_SAL_HOV, (240, 240, 240), fuente_boton)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False
                if event.key == pygame.K_RETURN:
                    return True
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if hover_jugar:
                    return True
                if hover_salir:
                    return False
        pygame.display.update()

def menu_pausa():
    ancho, alto = pantalla.get_size()
    btn_w, btn_h = 260, 55
    cx = ancho // 2
    btn_reanudar  = pygame.Rect(cx - btn_w // 2, alto // 2 - 40,  btn_w, btn_h)
    btn_reiniciar = pygame.Rect(cx - btn_w // 2, alto // 2 + 40,  btn_w, btn_h)
    btn_salir     = pygame.Rect(cx - btn_w // 2, alto // 2 + 120, btn_w, btn_h)
    fuente_pausa  = pygame.font.SysFont("impact", 60)
    overlay = pygame.Surface((ancho, alto), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 160))

    # Bucle del menú de pausa
    while True:
        relog.tick(60)
        pantalla.blit(overlay, (0, 0))
        tit = fuente_pausa.render("PAUSA", True, COLOR_TITULO)
        pantalla.blit(tit, tit.get_rect(center=(cx, alto // 2 - 120)))
        hover_reanudar  = dibujar_boton(pantalla, "REANUDAR",  btn_reanudar,  COLOR_BTN,     COLOR_BTN_HOV,     COLOR_TEXTO,     fuente_boton)
        hover_reiniciar = dibujar_boton(pantalla, "REINICIAR", btn_reiniciar, COLOR_BTN,     COLOR_BTN_HOV,     COLOR_TEXTO,     fuente_boton)
        hover_salir     = dibujar_boton(pantalla, "SALIR",     btn_salir,     COLOR_BTN_SAL, COLOR_BTN_SAL_HOV, (240, 240, 240), fuente_boton)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "salir"
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return "reanudar"
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if hover_reanudar:
                    return "reanudar"
                if hover_reiniciar:
                    return "reiniciar"
                if hover_salir:
                    return "salir"
        pygame.display.update()


# Mostramos el menú de inicio antes de entrar al juego
if not pantalla_inicio():
    pygame.quit()
    exit()


def hay_enemigo(fila, col, enemigos):
    # Revisa si ya hay un enemigo ocupando esa celda
    return any(e["fila"] == fila and e["col"] == col for e in enemigos)


def animar(entidad, moviendose, corriendo=False, direccion=None):
    ahora = pygame.time.get_ticks()

    # Si está disparando, dejamos que termine esa animación primero
    if getattr(entidad, "disparando", False):
        velocidad_frame = 80
        if ahora - entidad.tiempo_ultimo_frame > velocidad_frame:
            entidad.frame_actual += 1
            entidad.tiempo_ultimo_frame = ahora
            if entidad.frame_actual >= len(entidad.animaciones["Shooting"]):
                # Terminó la animación de disparo, volvemos a idle
                entidad.disparando = False
                entidad.frame_actual = 0
                entidad.animacion_actual = "idle"
        frame = entidad.animaciones["Shooting"][min(entidad.frame_actual, len(entidad.animaciones["Shooting"]) - 1)]
        entidad.image = pygame.transform.flip(frame, entidad.voltear, False)
        return

    # Elegimos la animación según si se está moviendo o no
    anim = "Running" if moviendose else "idle"
    velocidad_frame = 60 if corriendo else 100
    if anim != entidad.animacion_actual:
        entidad.animacion_actual = anim
        entidad.frame_actual = 0
        entidad.tiempo_ultimo_frame = ahora
    if ahora - entidad.tiempo_ultimo_frame > velocidad_frame:
        entidad.frame_actual = (entidad.frame_actual + 1) % len(entidad.animaciones[anim])
        entidad.tiempo_ultimo_frame = ahora

    # Voltear sprite según dirección horizontal
    if direccion == "izquierda":
        entidad.voltear = True
    elif direccion == "derecha":
        entidad.voltear = False
    frame = entidad.animaciones[entidad.animacion_actual][entidad.frame_actual]
    entidad.image = pygame.transform.flip(frame, entidad.voltear, False)  # flip horizontal si voltear es True


def dibujar_entidad(entidad, pantalla):
    pantalla.blit(entidad.image, entidad.forma)


def spawnar_enemigos():
    # Cada ronda trae un enemigo extra para que se ponga más difícil
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
    global jugador_fila, jugador_col, jugador, enemigos, mapa_grilla, ronda, mostrando_ronda, tiempo_mensaje_ronda
    mapa_grilla = construir_grilla_colision(mapa_tmx, filas, cols)
    mapa_grilla[1][1] = 0
    jugador_fila, jugador_col = 1, 1
    jugador = Personaje(0, 0)
    # Reiniciamos la ronda desde 1
    ronda = 1
    mostrando_ronda = False
    tiempo_mensaje_ronda = 0
    enemigos = spawnar_enemigos()


escala_colision = TILE_SIZE / mapa_tmx.tilewidth
colisiones = cargar_colisiones(mapa_tmx, escala_colision)

# Variables para el sistema de rondas
ronda = 1
mostrando_ronda = False
tiempo_mensaje_ronda = 0

reiniciar_partida()

# Variables de movimiento del jugador
mover_arriba = False
mover_abajo = False
mover_izquierda = False
mover_derecha = False
aumentar_velocidad = False
tiempo_ultimo_paso = 0

# Bucle principal
correr = True
while correr:
    relog.tick(FPS)

    pantalla.fill(COLOR_FONDO)

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

    # Movimiento del jugador basado en las teclas presionadas
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

        # Solo movemos si la celda es válida y no hay colisión
        if (0 <= fila_nueva < filas and
            0 <= col_nueva  < cols  and
            not hay_enemigo(fila_nueva, col_nueva, enemigos) and
            not verificar_colision(rect_jugador, 0, 0, rects_colision_offset, ancho_actual, alto_actual)):
            jugador_fila, jugador_col = fila_nueva, col_nueva
            tiempo_ultimo_paso = tiempo_actual

    moviendose = mover_arriba or mover_abajo or mover_izquierda or mover_derecha
    # Determinar dirección para voltear el sprite
    direccion = "izquierda" if mover_izquierda else "derecha" if mover_derecha else None
    animar(jugador, moviendose, aumentar_velocidad, direccion)
    dibujar_entidad(jugador, pantalla)

    # Actualizamos las balas y eliminamos enemigos que fueron impactados
    eliminados = jugador.actualizar_balas(mapa_grilla, enemigos)
    for e in eliminados:
        enemigos.remove(e)
    for bala in jugador.balas:
        bala.dibujar(pantalla)

    for enemigo in enemigos:
        animar(enemigo["obj"], False, False)
        dibujar_entidad(enemigo["obj"], pantalla)

    # Si no quedan enemigos, subimos la ronda
    if not enemigos and not mostrando_ronda:
        ronda += 1
        mostrando_ronda = True
        tiempo_mensaje_ronda = pygame.time.get_ticks()

    # Mostramos el mensaje de nueva ronda por 2 segundos
    if mostrando_ronda:
        overlay = pygame.Surface((ancho_actual, alto_actual), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 120))
        pantalla.blit(overlay, (0, 0))
        msg = fuente_ronda.render(f"RONDA {ronda}", True, COLOR_TITULO)
        pantalla.blit(msg, msg.get_rect(center=(ancho_actual // 2, alto_actual // 2)))
        if pygame.time.get_ticks() - tiempo_mensaje_ronda > 2000:
            mostrando_ronda = False
            enemigos = spawnar_enemigos()

    # Número de ronda actual en la esquina
    txt_ronda = fuente_boton.render(f"Ronda: {ronda}", True, COLOR_TITULO)
    pantalla.blit(txt_ronda, (10, 10))

    # Eventos del juego 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            correr = False
        
        # Click izquierdo para disparar hacia el mouse
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mx, my = pygame.mouse.get_pos()
            jugador.disparar(mx, my)

        # Eventos de teclado para movimiento y menú de pausa
        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_ESCAPE:
                accion = menu_pausa()

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

            # pantalla completa
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