import pygame
from constantes import ESCALA_ENEMIGO

# Función para escalar imágenes
def escalar_img(image, scale):
    w = image.get_width()
    h = image.get_height()
    return pygame.transform.scale(image, size=(w*scale, h*scale))

# Cargar animaciones de enemigos
animaciones = {}

animaciones["idle"] = []
for i in range(18):
    img = pygame.image.load(f"assets/images/enemigos/Idle/0_Zombie_Villager_Idle_{i:03}.png")
    img = escalar_img(img, ESCALA_ENEMIGO)
    animaciones["idle"].append(img)

animaciones["Running"] = []
for i in range(12):
    img = pygame.image.load(f"assets/images/enemigos/Running/0_Zombie_Villager_Running_{i:03}.png")
    img = escalar_img(img, ESCALA_ENEMIGO)
    animaciones["Running"].append(img)

animaciones["Dying"] = []
for i in range(15):
    img = pygame.image.load(f"assets/images/enemigos/Dying/0_Zombie_Villager_Dying_{i:03}.png")
    img = escalar_img(img, ESCALA_ENEMIGO)
    animaciones["Dying"].append(img)

animaciones["Run Slashing"] = []
for i in range(12):
    img = pygame.image.load(f"assets/images/enemigos/Run Slashing/0_Zombie_Villager_Run Slashing_{i:03}.png")
    img = escalar_img(img, ESCALA_ENEMIGO)
    animaciones["Run Slashing"].append(img)

animaciones["Run Throwing"] = []
for i in range(12):
    img = pygame.image.load(f"assets/images/enemigos/Run Throwing/0_Zombie_Villager_Run Throwing_{i:03}.png")
    img = escalar_img(img, ESCALA_ENEMIGO)
    animaciones["Run Throwing"].append(img)

animaciones["Slashing"] = []
for i in range(12):
    img = pygame.image.load(f"assets/images/enemigos/Slashing/0_Zombie_Villager_Slashing_{i:03}.png")
    img = escalar_img(img, ESCALA_ENEMIGO)
    animaciones["Slashing"].append(img)

animaciones["Walking"] = []
for i in range(24):
    img = pygame.image.load(f"assets/images/enemigos/Walking/0_Zombie_Villager_Walking_{i:03}.png")
    img = escalar_img(img, ESCALA_ENEMIGO)
    animaciones["Walking"].append(img)

# Clase para enemigos
class Enemigo:
    def __init__(self, x, y):
        self.animaciones = animaciones
        self.animacion_actual = "idle"
        self.frame_actual = 0
        self.image = self.animaciones[self.animacion_actual][self.frame_actual]
        self.forma = self.image.get_rect()
        self.forma.topleft = (x, y)
        self.tiempo_ultimo_frame = pygame.time.get_ticks()
        self.voltear = False  # indica si el sprite debe voltearse horizontalmente