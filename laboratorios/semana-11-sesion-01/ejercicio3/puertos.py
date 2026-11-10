"""Los puertos de la cancelacion. Ya estan completos: tu version por capas
tiene que usar exactamente estos nombres, porque las pruebas los usan."""


class RepositorioDeReservas:
    def agregar(self, estudiante, cancha, fecha, hora):
        """Guarda una reserva nueva y la devuelve como Reserva, con su id
        ("r-1", "r-2", ...)."""
        raise NotImplementedError

    def buscar(self, id_reserva):
        """La Reserva con ese id, o None si no existe."""
        raise NotImplementedError

    def borrar(self, id_reserva):
        raise NotImplementedError

    def registrar_penalizacion(self, estudiante):
        raise NotImplementedError

    def penalizaciones_de(self, estudiante):
        """Cuantas penalizaciones tiene registradas el estudiante."""
        raise NotImplementedError


class Reloj:
    def ahora(self):
        """La fecha ("AAAA-MM-DD") y la hora (un entero de 0 a 23) actuales,
        como una tupla (fecha, hora)."""
        raise NotImplementedError


class Notificador:
    def notificar(self, estudiante, mensaje):
        raise NotImplementedError
