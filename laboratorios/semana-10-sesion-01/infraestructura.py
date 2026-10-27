"""Las piezas de infraestructura del Ejercicio 3. Ya estan completas: no
las modifiques.

AlmacenCompartido simula un almacen de clave-valor al que se conectan
todos los servidores, como Redis. Igual que un servicio real, guarda una
copia de lo que recibe y entrega una copia de lo que tiene: modificar el
diccionario que devolvio leer(...) no cambia nada en el almacen hasta
que se vuelva a llamar guardar(...).

BalanceadorRoundRobin reparte cada llamada al siguiente servidor de la
lista, en orden, como el de la Semana 8.
"""


class AlmacenCompartido:
    def __init__(self):
        self.datos = {}

    def guardar(self, clave, valor):
        self.datos[clave] = dict(valor)

    def leer(self, clave):
        valor = self.datos.get(clave)
        if valor is None:
            return None
        return dict(valor)

    def borrar(self, clave):
        self.datos.pop(clave, None)


class BalanceadorRoundRobin:
    def __init__(self, servidores):
        self.servidores = servidores
        self.indice = 0

    def siguiente(self):
        servidor = self.servidores[self.indice % len(self.servidores)]
        self.indice = self.indice + 1
        return servidor

    def reemplazar(self, posicion, servidor_nuevo):
        self.servidores[posicion] = servidor_nuevo

    def agregar(self, servidor_nuevo):
        self.servidores.append(servidor_nuevo)
