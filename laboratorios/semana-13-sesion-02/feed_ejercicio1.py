"""Ejercicio 1: el feed de actividad, de dos formas.

Cada estudiante sigue equipos y espacios. Su feed muestra las publicaciones
mas recientes de lo que sigue. Las dos clases resuelven lo mismo con
estrategias opuestas:

- FeedEnEscritura (fan-out on write): al publicar, la publicacion se
  copia al feed de cada seguidor. Leer el feed es leer una sola lista.
- FeedEnLectura (fan-out on read): al publicar, la publicacion se guarda
  una sola vez, en la lista del autor. Leer el feed es juntar las listas
  de todo lo que se sigue.

Las dos guardan todo en un Almacen (actividad.py), que cuenta escrituras
y lecturas.

Corre el archivo con:

    python3 feed_ejercicio1.py

y las pruebas con:

    pytest test_feed_ejercicio1.py
"""

from actividad import Almacen, Publicacion, mas_recientes


class FeedEnEscritura:
    def __init__(self):
        self.almacen = Almacen()
        self.seguidores = {}

    def seguir(self, estudiante, autor):
        if autor not in self.seguidores:
            self.seguidores[autor] = []
        if estudiante not in self.seguidores[autor]:
            self.seguidores[autor].append(estudiante)

    def publicar(self, publicacion):
        # TODO 1: agrega la publicacion a la lista "feed:<estudiante>" de cada
        # seguidor del autor, con self.almacen.agregar.
        raise NotImplementedError

    def leer(self, estudiante, cantidad=10):
        # TODO 2: lee la lista "feed:<estudiante>" (una sola lectura) y devuelve
        # las `cantidad` mas recientes, con mas_recientes.
        raise NotImplementedError


class FeedEnLectura:
    def __init__(self):
        self.almacen = Almacen()
        self.seguidos = {}

    def seguir(self, estudiante, autor):
        if estudiante not in self.seguidos:
            self.seguidos[estudiante] = []
        if autor not in self.seguidos[estudiante]:
            self.seguidos[estudiante].append(autor)

    def publicar(self, publicacion):
        # TODO 3: agrega la publicacion una sola vez, a la lista "autor:<autor>".
        raise NotImplementedError

    def leer(self, estudiante, cantidad=10):
        # TODO 4: lee la lista "autor:<autor>" de cada autor que sigue el
        # estudiante (una lectura por autor), juntalas y devuelve las
        # `cantidad` mas recientes.
        raise NotImplementedError


def simular(feed):
    for i in range(10):
        feed.seguir("hincha-" + str(i), "futbol-arquitectura")
    for i in range(8000):
        feed.seguir("estudiante-" + str(i), "final-campeonato")
    for i in range(300):
        feed.seguir("ana", "equipo-" + str(i))

    feed.publicar(Publicacion("p1", "futbol-arquitectura", 100, "Partido el jueves 18:00"))
    print("  Escrituras despues del equipo de arquitectura:", feed.almacen.escrituras)
    feed.publicar(Publicacion("p2", "final-campeonato", 200, "La final es el sabado"))
    print("  Escrituras despues de la final:", feed.almacen.escrituras)

    for i in range(300):
        feed.publicar(Publicacion("e" + str(i), "equipo-" + str(i), 300 + i, "Entrenamiento"))
    antes = feed.almacen.lecturas
    primeras = feed.leer("ana", 3)
    print("  ana lee su feed:", primeras, "con", feed.almacen.lecturas - antes, "lecturas")
    print("  Escrituras en total:", feed.almacen.escrituras)


if __name__ == "__main__":
    print("Fan-out on write:")
    simular(FeedEnEscritura())
    print("Fan-out on read:")
    simular(FeedEnLectura())
