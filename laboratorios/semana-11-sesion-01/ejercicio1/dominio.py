"""El nucleo de ReservaU: que es una reserva y que reglas la gobiernan.

Este archivo no importa nada de afuera: ni sqlite3, ni http_simulado, ni
ningun otro modulo de esta carpeta. Las reglas se pueden probar sin base
de datos y sin HTTP.
"""

CANCHAS = ["cancha-1", "cancha-2", "cancha-3"]
HORAS_DEL_DIA = [7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]
MAXIMO_RESERVAS_POR_DIA = 2


class Reserva:
    def __init__(self, id_reserva, estudiante, cancha, fecha, hora):
        self.id = id_reserva
        self.estudiante = estudiante
        self.cancha = cancha
        self.fecha = fecha
        self.hora = hora

    def como_diccionario(self):
        return {
            "id": self.id,
            "estudiante": self.estudiante,
            "cancha": self.cancha,
            "fecha": self.fecha,
            "hora": self.hora,
        }


def motivo_de_rechazo(cancha, hora, hora_ocupada, reservas_del_dia):
    """Devuelve None si la reserva se puede hacer, o el motivo del rechazo.

    hora_ocupada: True si esa cancha ya tiene reserva a esa hora ese dia.
    reservas_del_dia: cuantas reservas tiene ya el estudiante ese dia.
    """
    # TODO 1: las cuatro reglas de reservas_acopladas.py, en el mismo
    # orden, sin SQL ni codigos HTTP: "cancha desconocida",
    # "fuera del horario", "hora ocupada", "limite diario alcanzado".
    return None
