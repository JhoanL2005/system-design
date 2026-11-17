"""Las piezas comunes del feed de actividad de ReservaU.

- Publicacion: algo que aparece en el feed (un partido programado, un
  espacio que se libero), con su autor (un equipo o un espacio), un
  momento (minutos desde el inicio del semestre) y un texto.
- Almacen: cuenta cuantas escrituras y lecturas se hacen, para comparar
  estrategias. En produccion cada escritura seria una fila en una base de
  datos o un elemento en una lista de Redis.

No lo modifiques: los tres ejercicios lo usan tal cual.
"""


class Publicacion:
    def __init__(self, id_publicacion, autor, momento, texto):
        self.id = id_publicacion
        self.autor = autor
        self.momento = momento
        self.texto = texto

    def __repr__(self):
        return self.id


class Almacen:
    def __init__(self):
        self.listas = {}
        self.escrituras = 0
        self.lecturas = 0

    def agregar(self, clave, publicacion):
        if clave not in self.listas:
            self.listas[clave] = []
        self.listas[clave].append(publicacion)
        self.escrituras = self.escrituras + 1

    def leer(self, clave):
        self.lecturas = self.lecturas + 1
        return self.listas.get(clave, [])[:]


def mas_recientes(publicaciones, cantidad):
    """Las `cantidad` publicaciones mas recientes, de la mas nueva a la mas vieja."""
    ordenadas = sorted(publicaciones, key=lambda p: p.momento, reverse=True)
    return ordenadas[:cantidad]
