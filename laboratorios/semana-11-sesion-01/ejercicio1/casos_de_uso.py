"""Los casos de uso de ReservaU: lo que la aplicacion hace, paso a paso.
Solo conoce el dominio y los puertos.
"""

from dominio import motivo_de_rechazo


class ReservarCancha:
    def __init__(self, repositorio):
        self.repositorio = repositorio

    def ejecutar(self, estudiante, cancha, fecha, hora):
        # TODO 2: pregunta al repositorio si la hora esta ocupada y cuantas
        # reservas tiene el estudiante ese dia, y decide con
        # motivo_de_rechazo. Si hay motivo, devuelve
        # {"estado": "rechazada", "motivo": motivo}. Si no, guarda y
        # devuelve {"estado": "confirmada", "reserva": la Reserva guardada}.
        raise NotImplementedError
