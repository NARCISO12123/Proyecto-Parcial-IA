# Nombre:  Narciso Beras 
# Matrícula:  24-EISN-2-026

import pygame
import heapq
import time
from constantes import ESCALA_ENEMIGO

#  UTILIDAD: escalar imágenes
def escalar_img(image, scale):
    w = image.get_width()
    h = image.get_height()
    return pygame.transform.scale(image, (int(w * scale), int(h * scale)))

#  CARGA DE ANIMACIONES 
animaciones = {}

# Animaciones de Idle - quieto
animaciones["idle"] = [
    escalar_img(pygame.image.load(f"assets/images/enemigos/Idle/0_Zombie_Villager_Idle_{i:03}.png"), ESCALA_ENEMIGO)
    for i in range(18)
]

# Animaciones de Running - corriendo
animaciones["Running"] = [
    escalar_img(pygame.image.load(f"assets/images/enemigos/Running/0_Zombie_Villager_Running_{i:03}.png"), ESCALA_ENEMIGO)
    for i in range(12)
]

# Animaciones de Dying - muriendo
animaciones["Dying"] = [
    escalar_img(pygame.image.load(f"assets/images/enemigos/Dying/0_Zombie_Villager_Dying_{i:03}.png"), ESCALA_ENEMIGO)
    for i in range(15)
]

# Animaciones de Run Slashing - corriendo y atacando
animaciones["Run Slashing"] = [
    escalar_img(pygame.image.load(f"assets/images/enemigos/Run Slashing/0_Zombie_Villager_Run Slashing_{i:03}.png"), ESCALA_ENEMIGO)
    for i in range(12)
]
# Animaciones de Slashing - atacando
animaciones["Slashing"] = [
    escalar_img(pygame.image.load(f"assets/images/enemigos/Slashing/0_Zombie_Villager_Slashing_{i:03}.png"), ESCALA_ENEMIGO)
    for i in range(12)
]

# Animaciones de Walking - caminando
animaciones["Walking"] = [
    escalar_img(pygame.image.load(f"assets/images/enemigos/Walking/0_Zombie_Villager_Walking_{i:03}.png"), ESCALA_ENEMIGO)
    for i in range(24)
]


#  Astar - para que los enemigos sigan al jugador evitando paredes 
def astar(grilla, inicio, fin):

    filas = len(grilla)
    cols  = len(grilla[0])

    def h(a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    open_set = []
    heapq.heappush(open_set, (h(inicio, fin), 0, inicio))
    came_from = {}
    g_score   = {inicio: 0}

    while open_set:
        _, g, actual = heapq.heappop(open_set)

        if actual == fin:
            # Reconstruir camino
            camino = []
            while actual in came_from:
                camino.append(actual)
                actual = came_from[actual]
            camino.reverse()
            return camino

        for df, dc in [(-1,0),(1,0),(0,-1),(0,1)]:
            vecino = (actual[0] + df, actual[1] + dc)
            if 0 <= vecino[0] < filas and 0 <= vecino[1] < cols:
                if grilla[vecino[0]][vecino[1]] == 0:
                    nuevo_g = g + 1
                    if nuevo_g < g_score.get(vecino, float("inf")):
                        g_score[vecino]   = nuevo_g
                        f = nuevo_g + h(vecino, fin)
                        heapq.heappush(open_set, (f, nuevo_g, vecino))
                        came_from[vecino] = actual
    return []


#  ÁRBOL DE COMPORTAMIENTO
class Selector:
    def __init__(self, hijos): self.hijos = hijos
    def ejecutar(self):
        for h in self.hijos:
            if h.ejecutar(): return True
        return False

class Secuencia:
    def __init__(self, hijos): self.hijos = hijos
    def ejecutar(self):
        for h in self.hijos:
            if not h.ejecutar(): return False
        return True

class Accion:
    def __init__(self, fn): self.fn = fn
    def ejecutar(self): return self.fn()

class Condicion:
    def __init__(self, fn): self.fn = fn
    def ejecutar(self): return self.fn()



#  CLASE ENEMIGO
class Enemigo:

    DIST_ATAQUE  = 1.5
    DIST_CORRER  = 8   
    INTERVALO_RUTA = 800   

    def __init__(self, x, y):
        self.animaciones      = animaciones
        self.animacion_actual = "idle"
        self.frame_actual     = 0
        self.image            = self.animaciones["idle"][0]
        self.forma            = self.image.get_rect()
        self.forma.topleft    = (x, y)
        self.tiempo_ultimo_frame = pygame.time.get_ticks()
        self.voltear          = False

        # Estado interno
        self.vivo             = True
        self.muriendo         = False  
        self.vida             = 100

        
        self.ruta             = []      
        self.tiempo_ruta      = 0       

        # Árbol de comportamiento
        self._construir_bt()

    # Árbol de comportamiento 
    def _construir_bt(self):
  
        self.bt = Selector([
            Secuencia([
                Condicion(lambda: self.muriendo),
                Accion(self._accion_morir),
            ]),
            Secuencia([
                Condicion(lambda: self._distancia_jugador() <= self.DIST_ATAQUE),
                Accion(self._accion_atacar),
            ]),
            Secuencia([
                Condicion(lambda: self._distancia_jugador() <= self.DIST_CORRER),
                Accion(self._accion_correr),
            ]),
            Accion(self._accion_caminar),
        ])

    def _distancia_jugador(self):
        if self._jugador_fila is None:
            return 9999
        return abs(self._fila - self._jugador_fila) + abs(self._col - self._jugador_col)

    def _orientar_hacia_jugador(self):
        if self._jugador_col is not None:
            self.voltear = self._jugador_col < self._col

    def _recalcular_ruta(self, grilla, otros_enemigos):
        
        ahora = pygame.time.get_ticks()
        if ahora - self.tiempo_ruta < self.INTERVALO_RUTA and self.ruta:
            return
        self.tiempo_ruta = ahora

        # Bloqueamos celdas ocupadas por otros enemigos para evitar solapamiento
        grilla_temp = [fila[:] for fila in grilla]
        for e in otros_enemigos:
            f, c = e["fila"], e["col"]
            if (f, c) != (self._fila, self._col):
                grilla_temp[f][c] = 1

        self.ruta = astar(
            grilla_temp,
            (self._fila, self._col),
            (self._jugador_fila, self._jugador_col)
        )

    def _avanzar_un_paso(self, grilla, otros_enemigos):
        if not self.ruta:
            return False
        siguiente = self.ruta[0]
        # Verificamos que nadie ocupe esa celda
        ocupada = any(e["fila"] == siguiente[0] and e["col"] == siguiente[1]
                      for e in otros_enemigos)
        if not ocupada and grilla[siguiente[0]][siguiente[1]] == 0:
            self._fila, self._col = siguiente
            self.ruta.pop(0)
            return True
        else:
            self.ruta = []  
            return False

    def _accion_morir(self):
        self._cambiar_animacion("Dying")
        return True

    def _accion_atacar(self):
        self._orientar_hacia_jugador()
        self._cambiar_animacion("Slashing")
        return True

    def _accion_correr(self):
        self._orientar_hacia_jugador()
        self._cambiar_animacion("Running")
        self._recalcular_ruta(self._grilla_actual, self._otros_enemigos)
        
        if pygame.time.get_ticks() - self._ultimo_paso > 120:  # ms entre pasos corriendo
            self._avanzar_un_paso(self._grilla_actual, self._otros_enemigos)
            self._ultimo_paso = pygame.time.get_ticks()
        return True

    def _accion_caminar(self):
        self._orientar_hacia_jugador()
        self._cambiar_animacion("Walking")
        self._recalcular_ruta(self._grilla_actual, self._otros_enemigos)
        
        if pygame.time.get_ticks() - self._ultimo_paso > 220:  # ms entre pasos caminando
            self._avanzar_un_paso(self._grilla_actual, self._otros_enemigos)
            self._ultimo_paso = pygame.time.get_ticks()
        return True

    def _cambiar_animacion(self, nombre):
        
        if self.animacion_actual != nombre:
            self.animacion_actual = nombre
            self.frame_actual     = 0

    def _animar(self, velocidad=100):
        ahora = pygame.time.get_ticks()
        
        if ahora - self.tiempo_ultimo_frame > velocidad:
            frames = self.animaciones[self.animacion_actual]
            self.frame_actual = (self.frame_actual + 1) % len(frames)
            self.tiempo_ultimo_frame = ahora

            # Si terminó la animación de muerte → marcar como no-vivo
            if self.animacion_actual == "Dying" and self.frame_actual == 0:
                self.vivo = False

        frame = self.animaciones[self.animacion_actual][self.frame_actual]
        self.image = pygame.transform.flip(frame, self.voltear, False)

    # ── Método principal llamado desde main.py ────
    def actualizar(self, fila, col, jugador_fila, jugador_col, grilla, otros_enemigos):

        # Guardamos contexto para usar en las acciones del árbol de comportamiento
        self._fila            = fila
        self._col             = col
        self._jugador_fila    = jugador_fila
        self._jugador_col     = jugador_col
        self._grilla_actual   = grilla
        self._otros_enemigos  = otros_enemigos
        if not hasattr(self, "_ultimo_paso"):
            self._ultimo_paso = pygame.time.get_ticks()

        # Ejecutar el árbol de comportamiento
        self.bt.ejecutar()

        # Animar el sprite según la animación activa
        vel = 80 if self.animacion_actual == "Running" else 120
        self._animar(vel)

        return self._fila, self._col

    def recibir_danio(self, cantidad=100):
        """Llamar cuando una bala impacta al enemigo."""
        self.vida -= cantidad
        if self.vida <= 0 and not self.muriendo:
            self.muriendo = True
            self._cambiar_animacion("Dying")