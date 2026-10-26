"""Ejercicio 1: una capa de cache cache-aside sobre la disponibilidad de
ReservaU, y cuanto tiempo ahorra.

Corre esto para ver el resultado:

    python3 cache_aside_ejercicio1.py

Y las pruebas con:

    pytest test_cache_aside_ejercicio1.py
"""

import time

from repositorio import RepositorioDeReservas


class ServicioSinCache:
    def __init__(self, repositorio):
        self.repositorio = repositorio

    def disponibilidad(self, cancha, fecha):
        return self.repositorio.consultar_disponibilidad(cancha, fecha)


class ServicioConCacheAside:
    def __init__(self, repositorio):
        self.repositorio = repositorio
        self.cache = {}
        self.aciertos = 0
        self.fallos = 0

    def disponibilidad(self, cancha, fecha):
        clave = (cancha, fecha)
        if clave in self.cache:
            self.aciertos = self.aciertos + 1
            return self.cache[clave]
        self.fallos = self.fallos + 1
        libres = self.repositorio.consultar_disponibilidad(cancha, fecha)
        self.cache[clave] = libres
        return libres

def medir(servicio, repeticiones):
    inicio = time.perf_counter()
    for _ in range(repeticiones):
        servicio.disponibilidad("Cancha 1", "2026-10-26")
    return time.perf_counter() - inicio


if __name__ == "__main__":
    sin_cache = ServicioSinCache(RepositorioDeReservas())
    print("Sin cache, 50 consultas:", round(medir(sin_cache, 50), 3), "segundos")

    repositorio = RepositorioDeReservas()
    con_cache = ServicioConCacheAside(repositorio)
    print("Con cache, 50 consultas:", round(medir(con_cache, 50), 3), "segundos")
    print("Aciertos:", con_cache.aciertos, "Fallos:", con_cache.fallos)
    print("Consultas que llegaron al repositorio:", repositorio.consultas)

    repositorio.registrar_reserva("Cancha 1", "2026-10-26", 18)
    print("Despues de reservar las 18, el cache dice libres:", con_cache.disponibilidad("Cancha 1", "2026-10-26"))
    print("El repositorio dice libres:", repositorio.consultar_disponibilidad("Cancha 1", "2026-10-26"))
