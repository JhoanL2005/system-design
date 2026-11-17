"""El caso de uso de reservar y cancelar: aplica las reglas de dominio.py
sobre un repositorio, el que se le pase. No sabe si es SQLite o un fake.
"""

from dominio import CUPO_SEMANAL, PUNTOS_PARA_BLOQUEAR, puntos_por_cancelar, semana_de


class ServicioDeReservas:
    def __init__(self, repositorio):
        self.repositorio = repositorio

    def motivo_de_rechazo(self, estudiante, fecha):
        """None si el estudiante puede reservar en esa fecha; si no, el motivo."""
        if self.repositorio.puntos_de(estudiante) >= PUNTOS_PARA_BLOQUEAR:
            return "estudiante bloqueado"
        if self.repositorio.contar_en_semana(estudiante, semana_de(fecha)) >= CUPO_SEMANAL:
            return "cupo semanal agotado"
        return None

    def reservar(self, id_reserva, estudiante, fecha):
        motivo = self.motivo_de_rechazo(estudiante, fecha)
        if motivo is not None:
            raise ValueError(motivo)
        self.repositorio.guardar(id_reserva, estudiante, fecha)

    def cancelar(self, id_reserva, minutos_de_anticipacion):
        """Borra la reserva y suma los puntos que corresponden al estudiante."""
        reserva = self.repositorio.buscar(id_reserva)
        if reserva is None:
            raise ValueError("reserva desconocida")
        estudiante = reserva[0]
        self.repositorio.borrar(id_reserva)
        self.repositorio.sumar_puntos(estudiante, puntos_por_cancelar(minutos_de_anticipacion))
