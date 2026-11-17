"""Donde ReservaU guarda sus datos. Dos implementaciones con los mismos
metodos:

- RepositorioSQLite: la de produccion, sobre una base SQLite (sqlite3, de
  la biblioteca estandar). Con ruta=":memory:" la base vive en memoria y
  desaparece al cerrar; con la ruta de un archivo, queda en el disco.
- RepositorioEnMemoria: un doble de prueba (fake), con diccionarios. Hace
  lo mismo, sin base de datos, para probar el servicio rapido.
"""

import sqlite3

from dominio import semana_de


class RepositorioSQLite:
    def __init__(self, ruta):
        self.conexion = sqlite3.connect(ruta)
        self.conexion.execute(
            "CREATE TABLE IF NOT EXISTS reservas (id TEXT PRIMARY KEY, estudiante TEXT, fecha TEXT, semana TEXT)")
        self.conexion.execute(
            "CREATE TABLE IF NOT EXISTS penalizaciones (estudiante TEXT, puntos INTEGER)")
        self.conexion.commit()

    def guardar(self, id_reserva, estudiante, fecha):
        self.conexion.execute("INSERT INTO reservas VALUES (?, ?, ?, ?)",
                              (id_reserva, estudiante, fecha, semana_de(fecha)))
        self.conexion.commit()

    def buscar(self, id_reserva):
        """(estudiante, fecha) de la reserva, o None si no existe."""
        fila = self.conexion.execute("SELECT estudiante, fecha FROM reservas WHERE id = ?",
                                     (id_reserva,)).fetchone()
        return fila

    def contar_en_semana(self, estudiante, semana):
        fila = self.conexion.execute("SELECT COUNT(*) FROM reservas WHERE estudiante = ? AND semana = ?",
                                     (estudiante, semana)).fetchone()
        return fila[0]

    def borrar(self, id_reserva):
        self.conexion.execute(
            "DELETE FROM reservas WHERE estudiante = (SELECT estudiante FROM reservas WHERE id = ?)",
            (id_reserva,))
        self.conexion.commit()

    def sumar_puntos(self, estudiante, puntos):
        self.conexion.execute("INSERT INTO penalizaciones VALUES (?, ?)", (estudiante, puntos))
        self.conexion.commit()

    def puntos_de(self, estudiante):
        fila = self.conexion.execute("SELECT COALESCE(SUM(puntos), 0) FROM penalizaciones WHERE estudiante = ?",
                                     (estudiante,)).fetchone()
        return fila[0]

    def cerrar(self):
        self.conexion.close()


class RepositorioEnMemoria:
    def __init__(self):
        self._reservas = {}
        self._puntos = {}

    def guardar(self, id_reserva, estudiante, fecha):
        if id_reserva in self._reservas:
            raise sqlite3.IntegrityError("UNIQUE constraint failed: reservas.id")
        self._reservas[id_reserva] = (estudiante, fecha)

    def buscar(self, id_reserva):
        return self._reservas.get(id_reserva)

    def contar_en_semana(self, estudiante, semana):
        total = 0
        for dueno, fecha in self._reservas.values():
            if dueno == estudiante and semana_de(fecha) == semana:
                total = total + 1
        return total

    def borrar(self, id_reserva):
        self._reservas.pop(id_reserva, None)

    def sumar_puntos(self, estudiante, puntos):
        self._puntos[estudiante] = self._puntos.get(estudiante, 0) + puntos

    def puntos_de(self, estudiante):
        return self._puntos.get(estudiante, 0)

    def cerrar(self):
        pass
