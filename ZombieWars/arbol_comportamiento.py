class NodoComportamiento:
    def __init__(self):
        self.hijos = []

    def agregar_hijo(self, hijo):
        self.hijos.append(hijo)

    def ejecutar(self):
        pass

class Selector(NodoComportamiento):
    """Ejecuta hijos hasta que uno retorne True"""
    def ejecutar(self):
        for hijo in self.hijos:
            if hijo.ejecutar():
                return True
        return False

class Secuencia(NodoComportamiento):
    """Ejecuta hijos mientras todos retornen True"""
    def ejecutar(self):
        for hijo in self.hijos:
            if not hijo.ejecutar():
                return False
        return True

class Accion(NodoComportamiento):
    """Ejecuta una función específica"""
    def __init__(self, accion):
        super().__init__()
        self.accion = accion

    def ejecutar(self):
        return self.accion()

class Invertir(NodoComportamiento):
    """Invierte el resultado del hijo"""
    def __init__(self, accion):
        super().__init__()
        self.agregar_hijo(accion)

    def ejecutar(self):
        return not self.hijos[0].ejecutar()

class Timer(NodoComportamiento):
    """Ejecuta cada N ticks"""
    def __init__(self, tiempo):
        super().__init__()
        self.tiempo = tiempo
        self.tiempo_restante = tiempo

    def ejecutar(self):
        if self.tiempo_restante > 0:
            self.tiempo_restante -= 1
            return False
        else:
            self.tiempo_restante = self.tiempo
            if self.hijos:
                self.hijos[0].ejecutar()
            return True