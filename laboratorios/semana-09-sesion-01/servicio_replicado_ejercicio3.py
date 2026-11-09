"""Ejercicio 3: decidir, lectura por lectura, si va a la primaria o a la
replica.

Corre las pruebas con:

    pytest test_servicio_replicado_ejercicio3.py

No cambies los nombres de la clase ni de los metodos, y lee siempre a
traves de self.base.leer_de_primaria() o self.base.leer_de_replica():
los tests cuentan en que nodo hiciste cada lectura.
"""

from datos_reservas import ReservaRegistrada


class ServicioDeReservasReplicado:
    def __init__(self, base):
        self.base = base
        self.siguiente_id = 1

    def cancha_disponible(self, campus, cancha, fecha, hora):
        for reserva in self.base.leer_de_primaria():
            if (reserva.campus == campus and reserva.cancha == cancha
                    and reserva.fecha == fecha and reserva.hora == hora):
                return False
        return True

    def reservar(self, id_estudiante, campus, cancha, fecha, hora):
        if not self.cancha_disponible(campus, cancha, fecha, hora):
            return None
        reserva = ReservaRegistrada(self.siguiente_id, id_estudiante, campus, cancha, fecha, hora)
        self.siguiente_id = self.siguiente_id + 1
        self.base.escribir(reserva)
        return reserva

    def mis_reservas(self, id_estudiante):
        if self.base.tiene_escrituras_pendientes_de(id_estudiante):
            todas = self.base.leer_de_primaria()
        else:
            todas = self.base.leer_de_replica()
        reservas = []
        for reserva in todas:
            if reserva.id_estudiante == id_estudiante:
                reservas.append(reserva)
        return reservas

    def ocupacion_del_campus(self, campus):
        cantidad = 0
        for reserva in self.base.leer_de_replica():
            if reserva.campus == campus:
                cantidad = cantidad + 1
        return cantidad
