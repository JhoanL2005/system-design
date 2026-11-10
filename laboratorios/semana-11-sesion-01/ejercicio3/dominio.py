"""El nucleo de la cancelacion de reservas. No importa nada de afuera."""

MINIMO_HORAS_DE_AVISO = 2


class Reserva:
    def __init__(self, id_reserva, estudiante, cancha, fecha, hora):
        self.id = id_reserva
        self.estudiante = estudiante
        self.cancha = cancha
        self.fecha = fecha
        self.hora = hora


def clasificar_cancelacion(fecha_reserva, hora_reserva, fecha_actual, hora_actual):
    """Devuelve "vencida" si la reserva ya empezo o ya paso, "tardia" si es
    el mismo dia con menos de MINIMO_HORAS_DE_AVISO horas de aviso, o
    "a tiempo". Las fechas son textos "AAAA-MM-DD": en ese formato,
    comparar dos fechas con < las compara en el tiempo."""
    # TODO 1: las mismas condiciones que cancelaciones_acopladas.py.
    return "a tiempo"
