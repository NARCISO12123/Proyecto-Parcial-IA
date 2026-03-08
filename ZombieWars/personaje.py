# Nombre:  Narciso Beras 
# Matrícula:  24-EISN-2-026

import pygame
import math
from constantes import ESCALA_JUGADOR

# Función para escalar imágenes
def escalar_img(image, scale):
    w = image.get_width()
    h = image.get_height()
    return pygame.transform.scale(image, size=(w*scale, h*scale))

# Cargar animaciones del personaje
animaciones = {}

# Cargar animaciones de Idle - quieto
animaciones["idle"] = []
for i in range(17):
    img = pygame.image.load(f"assets/images/personaje/Idle/0_Forest_Ranger_Idle_{i:03}.png")
    img = escalar_img(img, ESCALA_JUGADOR)
    animaciones["idle"].append(img)

# Cargar animaciones de Running - corriendo
animaciones["Running"] = []
for i in range(11):
    img = pygame.image.load(f"assets/images/personaje/Running/0_Forest_Ranger_Running_{i:03}.png")
    img = escalar_img(img, ESCALA_JUGADOR)
    animaciones["Running"].append(img)

# Cargar animaciones de Dying - muriendo
animaciones["Dying"] = []
for i in range(14):
    img = pygame.image.load(f"assets/images/personaje/Dying/0_Forest_Ranger_Dying_{i:03}.png")
    img = escalar_img(img, ESCALA_JUGADOR)
    animaciones["Dying"].append(img)

# Cargar animaciones de Run Shooting - corriendo y disparando
animaciones["Run Shooting"] = []
for i in range(12):
    img = pygame.image.load(f"assets/images/personaje/Run Shooting/0_Forest_Ranger_Run Shooting_{i:03}.png")
    img = escalar_img(img, ESCALA_JUGADOR)
    animaciones["Run Shooting"].append(img)

# Cargar animaciones de Shooting - disparando
animaciones["Shooting"] = []
for i in range(9):
    img = pygame.image.load(f"assets/images/personaje/Shooting/0_Forest_Ranger_Shooting_{i:03}.png")
    img = escalar_img(img, ESCALA_JUGADOR)
    animaciones["Shooting"].append(img)

animaciones["Walking"] = []
for i in range(23):
    img = pygame.image.load(f"assets/images/personaje/Walking/0_Forest_Ranger_Walking_{i:03}.png")
    img = escalar_img(img, ESCALA_JUGADOR)
    animaciones["Walking"].append(img)

# Clase para las balas disparadas por el personaje
class Bala:
    VELOCIDAD = 18
    DURACION  = 40
    COLOR     = (255, 230, 80)
    LARGO     = 8
    GROSOR    = 3

    def __init__(self, x, y, mx, my):
        self.x = float(x)
        self.y = float(y)
        dx = mx - x
        dy = my - y
        dist = math.hypot(dx, dy) or 1
        self.vx = dx / dist * self.VELOCIDAD
        self.vy = dy / dist * self.VELOCIDAD
        self.vida = self.DURACION

    def actualizar(self):
        self.x += self.vx
        self.y += self.vy
        self.vida -= 1

    def vivo(self):
        return self.vida > 0

    def dibujar(self, pantalla):
        x2 = int(self.x - self.vx * (self.LARGO / self.VELOCIDAD))
        y2 = int(self.y - self.vy * (self.LARGO / self.VELOCIDAD))
        pygame.draw.line(pantalla, self.COLOR, (int(self.x), int(self.y)), (x2, y2), self.GROSOR)

    def rect(self):
        return pygame.Rect(self.x - 4, self.y - 4, 8, 8)


# Clase para el personaje
class Personaje:
    VIDA_MAX = 100

    def __init__(self, x, y):
        self.animaciones = animaciones
        self.animacion_actual = "idle"
        self.frame_actual = 0
        self.image = self.animaciones[self.animacion_actual][self.frame_actual]
        self.forma = self.image.get_rect()
        self.forma.topleft = (x, y)
        self.tiempo_ultimo_frame = pygame.time.get_ticks()
        self.voltear   = False   
        self.disparando = False  
        self.balas = []

        # Sistema de vida
        self.vida     = self.VIDA_MAX
        self.muriendo = False   
        self.muerto   = False   

    #  Vida y daño

    def recibir_danio(self, cantidad):
        if self.muriendo or self.muerto:
            return
        self.vida = max(self.vida - cantidad, 0)
        
        if self.vida <= 0:
            self._iniciar_muerte()

    def _iniciar_muerte(self):
        self.muriendo = True
        self.disparando = False
        self.animacion_actual = "Dying"
        self.frame_actual = 0
        self.tiempo_ultimo_frame = pygame.time.get_ticks()

    # Disparar

    def disparar(self, mx, my):
        # No disparar si está muriendo
        if self.muriendo or self.muerto:
            return
        self.disparando = True
        self.animacion_actual = "Shooting"
        self.frame_actual = 0
        self.tiempo_ultimo_frame = pygame.time.get_ticks()
        bala = Bala(self.forma.centerx, self.forma.centery, mx, my)
        self.balas.append(bala)

    def actualizar_balas(self, mapa_grilla, enemigos):
        # Mover balas y detectar colisiones con enemigos y obstáculos
        eliminados = []
        vivas = []
        cols  = len(mapa_grilla[0]) if mapa_grilla else 0
        filas = len(mapa_grilla)

        for bala in self.balas:
            bala.actualizar()
            
            if not bala.vivo():
                continue

            col_b = int(bala.x) // (filas or 1)
            fil_b = int(bala.y) // (cols or 1)
            
            if not (0 <= fil_b < filas and 0 <= col_b < cols):
                continue
            
            if mapa_grilla[fil_b][col_b] == 1:
                continue

            impacto = False
            for e in enemigos:
            
                if bala.rect().colliderect(e["obj"].forma):
                    impacto = True
                    eliminados.append(e)
                    break

            if not impacto:
                vivas.append(bala)

        self.balas = vivas
        return eliminados

    # ── Animación de muerte (llamada desde main.py en animar()) ───

    def actualizar_muerte(self):
        if not self.muriendo:
            return
        ahora = pygame.time.get_ticks()
        
        if ahora - self.tiempo_ultimo_frame > 80:
            self.frame_actual += 1
            self.tiempo_ultimo_frame = ahora
            frames = self.animaciones["Dying"]
           
            if self.frame_actual >= len(frames):
                # Animación terminada
                self.frame_actual = len(frames) - 1
                self.muriendo = False
                self.muerto   = True
        
        frame = self.animaciones["Dying"][self.frame_actual]
        self.image = pygame.transform.flip(frame, self.voltear, False)