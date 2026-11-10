"""Los casos de uso de ReservaU: lo que la aplicacion hace, paso a paso.
Solo conoce el dominio y los puertos.
"""

from dominio import motivo_de_rechazo, texto_de_hora


class ReservarCancha:
    # TODO 1: el caso de uso recibe tambien un notificador (el puerto
    # Notificador), y al confirmar una reserva le envia al estudiante
    # "Reserva r-1 confirmada: cancha-1, 2026-11-10 a las 18:00" (con
    # texto_de_hora para la hora). Una reserva rechazada no notifica nada.
    def __init__(self, repositorio):
        self.repositorio = repositorio

    def ejecutar(self, estudiante, cancha, fecha, hora):
        hora_ocupada = self.repositorio.ocupada(cancha, fecha, hora)
        reservas_del_dia = self.repositorio.contar_del_estudiante(estudiante, fecha)
        motivo = motivo_de_rechazo(cancha, hora, hora_ocupada, reservas_del_dia)
        if motivo is not None:
            return {"estado": "rechazada", "motivo": motivo}
        reserva = self.repositorio.guardar(estudiante, cancha, fecha, hora)
        return {"estado": "confirmada", "reserva": reserva}
