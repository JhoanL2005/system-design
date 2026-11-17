"""Ejercicio 2: el calendario en vivo con varios servidores.

El dia de inscripciones hay demasiadas conexiones abiertas para un solo
servidor, asi que ReservaU las reparte entre varios ServidorDeConexiones.
Cada servidor tiene sus propios Canales (los del Ejercicio 1, por eso este
ejercicio necesita canales_ejercicio1.py completo) para sus conexiones.

Cuando cambia un calendario, el aviso entra por el BusEntreServidores (en
produccion seria, por ejemplo, Redis Pub/Sub): el bus se lo pasa solo a
los servidores que tienen al menos una conexion mirando ese tema, y cada
servidor lo reparte entre sus conexiones.

Ademas, un servidor no puede guardar para siempre las conexiones que se
cerraron: CanalesQueLimpian las saca de la lista la primera vez que
enviar devuelve False.

Corre el archivo con:

    python3 servidores_ejercicio2.py

y las pruebas con:

    pytest test_servidores_ejercicio2.py
"""

from canales_ejercicio1 import Canales
from conexiones import ConexionSimulada


class CanalesQueLimpian(Canales):
    def publicar(self, tema, mensaje):
        # TODO 1: como Canales.publicar, pero las conexiones a las que enviar
        # no les llego (estan cerradas) se quitan del tema. No quites
        # elementos de la lista mientras la recorres: junta primero las
        # cerradas y quitalas despues, con desuscribir.
        raise NotImplementedError


class BusEntreServidores:
    def __init__(self):
        self.servidores_por_tema = {}
        self.envios = 0

    def suscribir(self, tema, servidor):
        if tema not in self.servidores_por_tema:
            self.servidores_por_tema[tema] = []
        if servidor not in self.servidores_por_tema[tema]:
            self.servidores_por_tema[tema].append(servidor)

    def desuscribir(self, tema, servidor):
        if servidor in self.servidores_por_tema.get(tema, []):
            self.servidores_por_tema[tema].remove(servidor)

    def publicar(self, tema, mensaje):
        # TODO 4: para cada servidor suscrito al tema, llama
        # servidor.recibir_del_bus(tema, mensaje) y suma 1 a self.envios.
        # Devuelve el total de conexiones que recibieron el mensaje (la
        # suma de lo que devuelve cada servidor). Ojo: un servidor que se
        # queda sin conexiones se desuscribe del bus mientras recibe;
        # recorre una copia de la lista ([:]).
        raise NotImplementedError


class ServidorDeConexiones:
    def __init__(self, nombre, bus):
        self.nombre = nombre
        self.bus = bus
        self.canales = CanalesQueLimpian()

    def conectar(self, conexion, tema):
        # TODO 2: suscribe la conexion al tema en self.canales. Si es la
        # primera conexion de este servidor en ese tema, suscribe el
        # servidor al tema en el bus.
        raise NotImplementedError

    def desconectar(self, conexion, tema):
        # TODO 3: desuscribe la conexion del tema. Si el servidor se quedo sin
        # conexiones en ese tema, desuscribe el servidor del bus.
        raise NotImplementedError

    def recibir_del_bus(self, tema, mensaje):
        entregados = self.canales.publicar(tema, mensaje)
        if self.canales.suscriptores(tema) == 0:
            self.bus.desuscribir(tema, self)
        return entregados


if __name__ == "__main__":
    bus = BusEntreServidores()
    servidores = []
    for i in range(4):
        servidores.append(ServidorDeConexiones("servidor-" + str(i), bus))

    tema_1 = "cancha-1/2026-11-10"
    tema_3 = "cancha-3/2026-11-10"
    conexiones = []
    for i in range(1000):
        conexion = ConexionSimulada("estudiante-" + str(i))
        conexiones.append(conexion)
        servidores[i % 4].conectar(conexion, tema_1)
    unica = ConexionSimulada("entrenador")
    servidores[2].conectar(unica, tema_3)

    print("Conexiones que recibieron el aviso de cancha-1:", bus.publicar(tema_1, "ocupada 18-19"))
    print("Envios entre servidores:", bus.envios)
    print("Conexiones que recibieron el aviso de cancha-3:", bus.publicar(tema_3, "ocupada 9-10"))
    print("Envios entre servidores:", bus.envios)

    for i in range(0, 1000, 2):
        conexiones[i].cerrar()
    print("Con la mitad cerradas:", bus.publicar(tema_1, "libre 18-19"))
    print("Siguen suscritas en el servidor-0:", servidores[0].canales.suscriptores(tema_1))

    servidores[2].desconectar(unica, tema_3)
    print("Servidores escuchando cancha-3:", len(bus.servidores_por_tema[tema_3]))
