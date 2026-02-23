import pygame
import personaje
import Enemigos
from personaje import Personaje
from Enemigos import Enemigo

pygame.init()

# tamanio de la ventana
ancho = 1920
largo = 1080

# color de fondo
color_fondo = (0,0, 20)

# ventana donde corre el juego
pantalla = pygame.display.set_mode((ancho, largo))

# fps - frames de el juego
fps = 60
# --------------------------------------------------------------

# definir movimiento
mover_arriba = False
mover_abajo = False
mover_derecha = False 
mover_izquierda = False
jugador_corriendo = False

# metodo clock - Permite controlar
# los frames
relog = pygame.time.Clock()

# creamos el jugador 
Jugador = Personaje(100, 100, 5, 10)
# creamos enemigos
Zombie = Enemigo(200, 200)

correr = True
while correr == True:

    relog.tick(fps)


    # implementar color de fondo 
    pantalla.fill(color_fondo)
    
    # muestra el jugador en la pantalla
    Jugador.dibujar(pantalla)
    
    # muestra enemigo  
    Zombie.dibujar(pantalla)

    # calcular movimiento del jugador
    #  dice cuanto se va mover 

    delta_x = 0 # eje X - eje hirizontal izquierda o derecha
    delta_y = 0 # eje Y - Eje vertical arriba o abajo

    if mover_arriba == True:
        
        delta_y = -Jugador.velocidad

    if mover_abajo == True:
        
        delta_y = Jugador.velocidad

    
    if mover_derecha == True:
        
        delta_x = Jugador.velocidad


    if mover_izquierda == True:
        
        delta_x = -Jugador.velocidad


    if jugador_corriendo == True:
        
        Jugador.AumentarVelocidad()
    
    else:
        Jugador.detener()

        
 # correr Juego 
    for event in pygame.event.get():

        if event.type == pygame.QUIT:

            correr = False
        
        # crear moviento

        # registra cuando presionas una tecla:
        if event.type == pygame.KEYDOWN:

        # cuando presiona una de las teclas cambia 
        # la variable a True activando el movimiento
            if event.key == pygame.K_a:
                mover_izquierda = True

            if event.key == pygame.K_s:
                mover_abajo = True

            if event.key == pygame.K_d:
                mover_derecha = True

            if event.key == pygame.K_w:
                mover_arriba = True
            
            if event.key == pygame.K_LSHIFT:
                jugador_corriendo = True

        # registra cuando sueltas una tecla:
        # caundo soltamos la tecla vuelve a False
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
                jugador_corriendo = False

    # mover jugador 
    Jugador.mover(delta_x, delta_y)
    
    pygame.display.update()

pygame.quit


# prueba de guardado