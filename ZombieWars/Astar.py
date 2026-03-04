import heapq
import time

class Nodo:
    def __init__(self, dato, padre=None, distancia=0):
        self.dato = dato
        self.padre = padre
        self.H = distancia
        if padre == None:
            self.profundidad = 0
        else:
            self.profundidad = padre.profundidad + 1

    def GenerarSucesores(self):
        return self.dato.GenerarSucesores()

    def __eq__(self, __o) -> bool:
        if isinstance(__o, Nodo):
            return self.dato == __o.dato
        if isinstance(__o, type(self.dato)):
            return self.dato == __o
        return False

    def __lt__(self, __o) -> bool:
        if isinstance(__o, Nodo):
            return self.Heuristica() < __o.Heuristica()
        return False

    def __gt__(self, __o) -> bool:
        if isinstance(__o, Nodo):
            return self.Heuristica() > __o.Heuristica()
        return False

    def Heuristica(self):
        return self.H + self.profundidad

    def __hash__(self) -> int:
        hsh = str(self.dato)
        return hash(hsh)

    def __str__(self):
        return str(self.dato.__str__())


def Astar(estado_inicial, estado_final):
    totalnodos = 1
    nodoactual = Nodo(estado_inicial, None, estado_inicial.Costo(estado_final))
    nodosgenerado = []
    nodosvisitados = set()
    heapq.heapify(nodosgenerado)

    inicio = time.perf_counter()

    while nodoactual.dato != estado_final:
        sucesores = nodoactual.GenerarSucesores()
        totalnodos += len(sucesores)

        for sucesor in sucesores:
            temp = Nodo(sucesor, nodoactual, sucesor.Costo(estado_final))
            if temp not in nodosvisitados:
                heapq.heappush(nodosgenerado, temp)
        
        nodosvisitados.add(nodoactual)

        while nodoactual in nodosvisitados:
            nodoactual = heapq.heappop(nodosgenerado)
    
    camino = []
    while nodoactual:
        camino.append(nodoactual.dato)
        nodoactual = nodoactual.padre
    camino.reverse()
    
    fin = time.perf_counter()
    return camino, totalnodos, fin - inicio


class EstadoMapa:
    """Clase que representa un estado del mapa"""
    def __init__(self, configuracion, cordenadas, enemigos_pos=None):
        self.configuracion = configuracion
        self.cordenadas = cordenadas
        self.tamano = len(configuracion)
        self.enemigos_pos = enemigos_pos or []

    def GenerarSucesores(self):
        sucesores = []
        movimientos_validos = [[0, 1], [1, 0], [0, -1], [-1, 0]]

        for movimiento in movimientos_validos:
            x = self.cordenadas[0] + movimiento[0]
            y = self.cordenadas[1] + movimiento[1]

            if x >= 0 and x < self.tamano and y >= 0 and y < len(self.configuracion[0]):
                if self.configuracion[x][y] != 1:
                    if (x, y) not in self.enemigos_pos:
                        nueva_configuracion = self.configuracion
                        sucesores.append(EstadoMapa(nueva_configuracion, [x, y], self.enemigos_pos))

        return sucesores

    def __eq__(self, __o: object) -> bool:
        if isinstance(__o, EstadoMapa):
            return self.cordenadas == __o.cordenadas
        return self.cordenadas == __o

    def __hash__(self) -> int:
        return hash(str(self.cordenadas))

    def __str__(self):
        return str(self.cordenadas)

    def Costo(self, estado_final):
        """Distancia Manhattan"""
        return abs(self.cordenadas[0] - estado_final.cordenadas[0]) + abs(self.cordenadas[1] - estado_final.cordenadas[1])