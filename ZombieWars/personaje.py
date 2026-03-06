import pygame
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

# Cargar animaciones de Run Slashing - corriendo y atacando
animaciones["Run Shooting"] = []
for i in range(12):
    img = pygame.image.load(f"assets/images/personaje/Run Shooting/0_Forest_Ranger_Run Shooting_{i:03}.png")
    img = escalar_img(img, ESCALA_JUGADOR)
    animaciones["Run Shooting"].append(img)
    
# Cargar animaciones de Run Throwing - corriendo y lanzando
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

# Clase para el personaje
class Personaje:
    def __init__(self, x, y):
        self.animaciones = animaciones
        self.animacion_actual = "idle"
        self.frame_actual = 0
        self.image = self.animaciones[self.animacion_actual][self.frame_actual]
        self.forma = self.image.get_rect()
        self.forma.topleft = (x, y)
        self.tiempo_ultimo_frame = pygame.time.get_ticks()