import pygame
from constantes import *

# Colores del menú
COLOR_FONDO       = (25, 8, 40)
COLOR_TITULO      = (200, 255, 100)
COLOR_BTN         = (200, 255, 100)
COLOR_BTN_HOV     = (220, 255, 140)
COLOR_BTN_SAL     = (180, 60, 60)
COLOR_BTN_SAL_HOV = (220, 90, 90)
COLOR_TEXTO       = (25, 8, 40)

# Fuentes
try:
    fuente_titulo   = pygame.font.SysFont("impact", 80)
    fuente_boton    = pygame.font.SysFont("impact", 32)
    fuente_ronda    = pygame.font.SysFont("impact", 60)
    fuente_gameover = pygame.font.SysFont("impact", 90)

except Exception:
    fuente_titulo   = pygame.font.Font(None, 80)
    fuente_boton    = pygame.font.Font(None, 32)
    fuente_ronda    = pygame.font.Font(None, 60)
    fuente_gameover = pygame.font.Font(None, 90)

# Funciones para dibujar pantallas y botones
def dibujar_boton(surface, texto, rect, color_base, color_hover, color_txt, fuente):
    hover = rect.collidepoint(pygame.mouse.get_pos())
    pygame.draw.rect(surface, color_hover if hover else color_base, rect, border_radius=6)
    txt_surf = fuente.render(texto, True, color_txt)
    surface.blit(txt_surf, txt_surf.get_rect(center=rect.center))
    return hover


def pantalla_inicio(pantalla, relog):
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


def pantalla_game_over(pantalla, relog):
    ancho, alto = pantalla.get_size()
    btn_w, btn_h = 260, 55
    cx = ancho // 2
    btn_reiniciar = pygame.Rect(cx - btn_w // 2, alto // 2 + 40,  btn_w, btn_h)
    btn_salir     = pygame.Rect(cx - btn_w // 2, alto // 2 + 120, btn_w, btn_h)
    
    # Bucle del menú de Game Over
    while True:
        relog.tick(60)
        overlay = pygame.Surface((ancho, alto), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        pantalla.blit(overlay, (0, 0))
        txt_go = fuente_gameover.render("GAME OVER", True, (220, 40, 40))
        pantalla.blit(txt_go, txt_go.get_rect(center=(cx, alto // 2 - 60)))
        hover_reiniciar = dibujar_boton(pantalla, "REINICIAR", btn_reiniciar, COLOR_BTN,     COLOR_BTN_HOV,     COLOR_TEXTO,     fuente_boton)
        hover_salir     = dibujar_boton(pantalla, "SALIR",     btn_salir,     COLOR_BTN_SAL, COLOR_BTN_SAL_HOV, (240, 240, 240), fuente_boton)
    
        # bucle de eventos 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return False
            
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            
                if hover_reiniciar:
                    return True
            
                if hover_salir:
                    return False
        pygame.display.update()


def menu_pausa(pantalla, relog):
    
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

# Pantallas de juego
def dibujar_mensaje_ronda(pantalla, ronda):
    ancho, alto = pantalla.get_size()
    overlay = pygame.Surface((ancho, alto), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 120))
    pantalla.blit(overlay, (0, 0))
    msg = fuente_ronda.render(f"RONDA {ronda}", True, COLOR_TITULO)
    pantalla.blit(msg, msg.get_rect(center=(ancho // 2, alto // 2)))