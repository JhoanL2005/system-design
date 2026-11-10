"""Ejercicio 1: la jerarquia de espacios del campus.

ReservaU crece: ademas de las canchas del complejo deportivo, se reservan
las salas de estudio de la biblioteca, que estan repartidas por pisos.

Parte A (ya escrita, no la cambies): Campus, Edificio y Espacio como tres
clases distintas, y una busqueda que recorre un nivel por ciclo y pregunta
en cada nivel de que tipo es cada cosa. La biblioteca tiene pisos, y
cuando se escribio la busqueda no los tenia.

Parte B (TODO 1 a 3): una sola interfaz, Recurso, para un espacio simple
y para un grupo de recursos. La busqueda no pregunta nada.

Corre el archivo con:

    python3 espacios_ejercicio1.py

y las pruebas con:

    pytest test_espacios_ejercicio1.py
"""

from reservas import CalendarioDeCancha

FECHA = "2026-11-10"


# ---------------------------------------------------------------- Parte A

class Espacio:
    def __init__(self, nombre, capacidad):
        self.nombre = nombre
        self.capacidad = capacidad
        self.calendario = CalendarioDeCancha(nombre, FECHA)


class Piso:
    def __init__(self, nombre):
        self.nombre = nombre
        self.espacios = []


class Edificio:
    def __init__(self, nombre):
        self.nombre = nombre
        self.espacios = []


class Campus:
    def __init__(self, nombre):
        self.nombre = nombre
        self.edificios = []


def buscar_libres_preguntando(campus, inicio, fin):
    libres = []
    for edificio in campus.edificios:
        for cosa in edificio.espacios:
            if isinstance(cosa, Espacio):
                if cosa.calendario.esta_libre(inicio, fin):
                    libres.append(cosa.nombre)
    return libres


def armar_campus_por_niveles():
    complejo = Edificio("Complejo deportivo")
    for nombre, capacidad in [("cancha-1", 12), ("cancha-2", 12), ("cancha-3", 10)]:
        complejo.espacios.append(Espacio(nombre, capacidad))
    piso_1 = Piso("Piso 1")
    piso_1.espacios.append(Espacio("sala-101", 4))
    piso_1.espacios.append(Espacio("sala-102", 6))
    piso_2 = Piso("Piso 2")
    piso_2.espacios.append(Espacio("sala-201", 8))
    biblioteca = Edificio("Biblioteca")
    biblioteca.espacios.append(piso_1)
    biblioteca.espacios.append(piso_2)
    campus = Campus("Campus Cumbaya")
    campus.edificios.append(complejo)
    campus.edificios.append(biblioteca)
    complejo.espacios[0].calendario.reservar("r-1", "ana", 18, 19)
    piso_1.espacios[1].calendario.reservar("r-2", "carla", 18, 19)
    return campus


# ---------------------------------------------------------------- Parte B

class Recurso:
    """Lo que tienen en comun un espacio simple y un grupo de recursos."""

    def __init__(self, nombre):
        self.nombre = nombre

    def libres(self, inicio, fin):
        """Los nombres de los espacios simples libres en esa franja."""
        raise NotImplementedError

    def capacidad_total(self):
        """Cuantas personas caben, sumando todos los espacios simples."""
        raise NotImplementedError


class EspacioSimple(Recurso):
    def __init__(self, nombre, capacidad):
        super().__init__(nombre)
        self.capacidad = capacidad
        self.calendario = CalendarioDeCancha(nombre, FECHA)

    # TODO 1: libres devuelve [self.nombre] si el calendario esta libre en
    # esa franja, o una lista vacia si no. capacidad_total devuelve la
    # capacidad.


class GrupoDeRecursos(Recurso):
    def __init__(self, nombre):
        super().__init__(nombre)
        self.hijos = []

    def agregar(self, hijo):
        self.hijos.append(hijo)

    # TODO 2: libres junta, en orden, lo que devuelve libres de cada hijo.
    # No preguntes de que clase es cada hijo.

    # TODO 3: capacidad_total suma la capacidad_total de cada hijo.


def armar_campus():
    canchas = []
    complejo = GrupoDeRecursos("Complejo deportivo")
    for nombre, capacidad in [("cancha-1", 12), ("cancha-2", 12), ("cancha-3", 10)]:
        cancha = EspacioSimple(nombre, capacidad)
        complejo.agregar(cancha)
        canchas.append(cancha)
    piso_1 = GrupoDeRecursos("Piso 1")
    sala_101 = EspacioSimple("sala-101", 4)
    sala_102 = EspacioSimple("sala-102", 6)
    piso_1.agregar(sala_101)
    piso_1.agregar(sala_102)
    piso_2 = GrupoDeRecursos("Piso 2")
    piso_2.agregar(EspacioSimple("sala-201", 8))
    biblioteca = GrupoDeRecursos("Biblioteca")
    biblioteca.agregar(piso_1)
    biblioteca.agregar(piso_2)
    campus = GrupoDeRecursos("Campus Cumbaya")
    campus.agregar(complejo)
    campus.agregar(biblioteca)
    canchas[0].calendario.reservar("r-1", "ana", 18, 19)
    sala_102.calendario.reservar("r-2", "carla", 18, 19)
    return campus, biblioteca


if __name__ == "__main__":
    print("Parte A, preguntando en cada nivel:")
    print("  Libres de 18 a 19:", buscar_libres_preguntando(armar_campus_por_niveles(), 18, 19))

    print("Parte B, con una sola interfaz:")
    campus, biblioteca = armar_campus()
    print("  Libres de 18 a 19:", campus.libres(18, 19))
    print("  Libres de 18 a 19 en la biblioteca:", biblioteca.libres(18, 19))
    print("  Capacidad del campus:", campus.capacidad_total())
    print("  Capacidad de la biblioteca:", biblioteca.capacidad_total())
