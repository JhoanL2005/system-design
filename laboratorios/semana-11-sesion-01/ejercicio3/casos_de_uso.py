"""El caso de uso de cancelar una reserva. Solo puede importar dominio."""

from dominio import clasificar_cancelacion


class CancelarReserva:
    def __init__(self, repositorio, reloj, notificador):
        self.repositorio = repositorio
        self.reloj = reloj
        self.notificador = notificador

    def ejecutar(self, id_reserva, estudiante):
        # TODO 2: el mismo flujo de ServicioDeCancelaciones.cancelar, con los
        # mismos resultados y los mismos mensajes, usando solo los tres
        # puertos y clasificar_cancelacion.
        raise NotImplementedError
