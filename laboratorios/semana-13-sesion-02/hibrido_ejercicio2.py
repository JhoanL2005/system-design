"""Ejercicio 2: el feed hibrido.

Ninguna de las dos estrategias del Ejercicio 1 sirve para todos los
autores: copiar la final del campeonato a 8000 feeds es caro al
publicar, y juntar 300 listas cada vez que ana abre la app es caro al
leer. FeedHibrido usa las dos:

- Un autor es masivo si tiene mas de `umbral` seguidores.
- Las publicaciones de un autor que no es masivo se copian al feed de
  cada seguidor ("feed:<estudiante>"), como en FeedEnEscritura.
- Las de un autor masivo se guardan una sola vez ("autor:<autor>"), como
  en FeedEnLectura.
- Leer el feed es leer la lista propia y la de cada autor masivo que se
  sigue, juntarlas y quedarse con las mas recientes.

Corre el archivo con:

    python3 hibrido_ejercicio2.py

y las pruebas con:

    pytest test_hibrido_ejercicio2.py
"""

from actividad import Almacen, Publicacion, mas_recientes
from feed_ejercicio1 import FeedEnEscritura, FeedEnLectura


class FeedHibrido:
    def __init__(self, umbral=1000):
        self.umbral = umbral
        self.almacen = Almacen()
        self.seguidores = {}
        self.seguidos = {}

    def seguir(self, estudiante, autor):
        if autor not in self.seguidores:
            self.seguidores[autor] = []
        if estudiante not in self.seguidores[autor]:
            self.seguidores[autor].append(estudiante)
        if estudiante not in self.seguidos:
            self.seguidos[estudiante] = []
        if autor not in self.seguidos[estudiante]:
            self.seguidos[estudiante].append(autor)

    def es_masivo(self, autor):
        # TODO 1: True si el autor tiene mas de self.umbral seguidores.
        raise NotImplementedError

    def publicar(self, publicacion):
        # TODO 2: si el autor es masivo, una escritura en "autor:<autor>"; si
        # no, una escritura en "feed:<estudiante>" por cada seguidor.
        raise NotImplementedError

    def leer(self, estudiante, cantidad=10):
        # TODO 3: lee "feed:<estudiante>" y "autor:<autor>" de cada autor masivo
        # que sigue, juntalas y devuelve las `cantidad` mas recientes.
        raise NotImplementedError


def un_dia(feed):
    """Un dia de inscripciones: quien sigue que, cuanto se publica y cuanto se lee."""
    for i in range(8000):
        feed.seguir("estudiante-" + str(i), "final-campeonato")
    for i in range(8000):
        for k in range(30):
            equipo = (i // 20 + 13 * k) % 400
            feed.seguir("estudiante-" + str(i), "equipo-" + str(equipo))
    momento = 0
    for vuelta in range(3):
        for equipo in range(400):
            momento = momento + 1
            feed.publicar(Publicacion("e" + str(momento), "equipo-" + str(equipo), momento, "Entrenamiento"))
    for vuelta in range(5):
        momento = momento + 1
        feed.publicar(Publicacion("f" + str(vuelta), "final-campeonato", momento, "Novedades de la final"))
    escrituras = feed.almacen.escrituras
    for vuelta in range(10):
        for i in range(8000):
            feed.leer("estudiante-" + str(i), 10)
    return escrituras, feed.almacen.lecturas


if __name__ == "__main__":
    print("Un dia, 8000 estudiantes que abren el feed 10 veces:")
    for nombre, feed in [("Fan-out on write", FeedEnEscritura()), ("Fan-out on read", FeedEnLectura()), ("Hibrido", FeedHibrido())]:
        escrituras, lecturas = un_dia(feed)
        print(" ", nombre + ":", escrituras, "escrituras,", lecturas, "lecturas")

    hibrido = FeedHibrido(umbral=2)
    for estudiante in ["ana", "beto", "carla"]:
        hibrido.seguir(estudiante, "final-campeonato")
    hibrido.seguir("ana", "futbol-arquitectura")
    hibrido.publicar(Publicacion("p1", "futbol-arquitectura", 10, "Partido el jueves"))
    hibrido.publicar(Publicacion("p2", "final-campeonato", 20, "La final es el sabado"))
    print("La final es masiva:", hibrido.es_masivo("final-campeonato"))
    print("Feed de ana:", hibrido.leer("ana"))
    print("Feed de beto:", hibrido.leer("beto"))
