"""Ejercicio 3, punto de partida: la cancelacion de reservas de ReservaU
tal como esta hoy. Una sola clase lee y escribe en SQLite, mira la hora
del computador y envia el correo.

Las reglas:
- Solo el estudiante que hizo la reserva puede cancelarla.
- Una reserva que ya empezo, o que ya paso, no se puede cancelar.
- Cancelar el mismo dia con menos de 2 horas de aviso se permite, pero
  registra una penalizacion al estudiante.
- Toda cancelacion le envia un correo al estudiante.

No lo modifiques: es el comportamiento que tu version por capas tiene que
conservar. Corre esto para verlo (el resultado depende de la hora a la
que lo corras):

    python3 cancelaciones_acopladas.py
"""

import sqlite3
import time

import correo_simulado

MINIMO_HORAS_DE_AVISO = 2


class ServicioDeCancelaciones:
    def __init__(self, ruta_base_de_datos):
        self.conexion = sqlite3.connect(ruta_base_de_datos)
        self.conexion.execute(
            "CREATE TABLE IF NOT EXISTS reservas ("
            "id INTEGER PRIMARY KEY AUTOINCREMENT, "
            "estudiante TEXT, cancha TEXT, fecha TEXT, hora INTEGER)"
        )
        self.conexion.execute("CREATE TABLE IF NOT EXISTS penalizaciones (estudiante TEXT)")

    def agregar_reserva(self, estudiante, cancha, fecha, hora):
        cursor = self.conexion.execute(
            "INSERT INTO reservas (estudiante, cancha, fecha, hora) VALUES (?, ?, ?, ?)",
            (estudiante, cancha, fecha, hora),
        )
        self.conexion.commit()
        return "r-" + str(cursor.lastrowid)

    def cancelar(self, id_reserva, estudiante):
        numero = int(id_reserva[2:])
        fila = self.conexion.execute(
            "SELECT estudiante, fecha, hora FROM reservas WHERE id = ?", (numero,)
        ).fetchone()
        if fila is None:
            return {"estado": "rechazada", "motivo": "reserva desconocida"}
        if fila[0] != estudiante:
            return {"estado": "rechazada", "motivo": "no es tu reserva"}
        fecha = fila[1]
        hora = fila[2]
        hoy = time.strftime("%Y-%m-%d")
        hora_actual = time.localtime().tm_hour
        if fecha < hoy or (fecha == hoy and hora <= hora_actual):
            return {"estado": "rechazada", "motivo": "la reserva ya empezo"}
        tardia = fecha == hoy and hora - hora_actual < MINIMO_HORAS_DE_AVISO
        self.conexion.execute("DELETE FROM reservas WHERE id = ?", (numero,))
        if tardia:
            self.conexion.execute("INSERT INTO penalizaciones (estudiante) VALUES (?)", (estudiante,))
            correo_simulado.enviar_correo(estudiante, "Reserva " + id_reserva + " cancelada con penalizacion por aviso tardio")
        else:
            correo_simulado.enviar_correo(estudiante, "Reserva " + id_reserva + " cancelada")
        self.conexion.commit()
        return {"estado": "cancelada", "penalizacion": tardia}

    def penalizaciones_de(self, estudiante):
        fila = self.conexion.execute(
            "SELECT COUNT(*) FROM penalizaciones WHERE estudiante = ?", (estudiante,)
        ).fetchone()
        return fila[0]


if __name__ == "__main__":
    servicio = ServicioDeCancelaciones(":memory:")
    hoy = time.strftime("%Y-%m-%d")
    hora_actual = time.localtime().tm_hour
    print("Ahora:", hoy, "a las", hora_actual)
    id_ana = servicio.agregar_reserva("ana", "cancha-1", "2099-01-15", 18)
    id_beto = servicio.agregar_reserva("beto", "cancha-2", hoy, hora_actual + 1)
    print(servicio.cancelar(id_ana, "beto"))
    print(servicio.cancelar(id_ana, "ana"))
    print(servicio.cancelar(id_beto, "beto"))
    print(servicio.cancelar("r-9", "ana"))
    print("Penalizaciones de beto:", servicio.penalizaciones_de("beto"))
