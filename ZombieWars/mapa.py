import pygame
import pytmx

def cargar_mapa_tmx(ruta):
    datos = pytmx.load_pygame(ruta, pixelalpha=True)
    return datos, datos.height, datos.width

def construir_grilla_colision(datos_tmx, filas, cols):
    mapa = [[0]*cols for _ in range(filas)]
    try:
        capa = datos_tmx.get_layer_by_name("Colision")
        for x, y, gid in capa:
            if gid != 0:
                mapa[y][x] = 1
    except Exception:
        pass
    return mapa

def cargar_colisiones(datos_tmx, escala):
    colisiones = []
    for layer in datos_tmx.layers:
        if isinstance(layer, pytmx.TiledObjectGroup):
            if layer.name.lower() == "colisiones":
                for obj in layer:
                    rect = pygame.Rect(
                        int(obj.x * escala),
                        int(obj.y * escala),
                        int(obj.width * escala),
                        int(obj.height * escala),
                    )
                    colisiones.append(rect)
    return colisiones

def verificar_colision(rect_jugador, dx, dy, colisiones, ancho_px, alto_px):
    rect_temp = rect_jugador.copy()
    rect_temp.x += dx
    rect_temp.y += dy
    for colision in colisiones:
        if rect_temp.colliderect(colision):
            return True
    if (rect_temp.left < 0 or rect_temp.right > ancho_px or
        rect_temp.top < 0 or rect_temp.bottom > alto_px):
        return True
    return False

def dibujar_mapa(pantalla, datos_tmx, tile_size, offset_x, offset_y):
    for capa in datos_tmx.visible_layers:
        if isinstance(capa, pytmx.TiledTileLayer):
            for x, y, imagen in capa.tiles():
                if imagen and isinstance(imagen, pygame.Surface):
                    try:
                        tile = pygame.transform.scale(imagen, (tile_size, tile_size))
                        pantalla.blit(tile, (offset_x + x * tile_size, offset_y + y * tile_size))
                    except Exception:
                        pass