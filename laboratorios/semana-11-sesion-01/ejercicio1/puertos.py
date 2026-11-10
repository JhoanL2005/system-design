"""Los puertos de ReservaU: lo que el caso de uso necesita del mundo de
afuera, dicho en terminos del negocio. Cada metodo lanza
NotImplementedError: un adaptador hereda de la clase y lo implementa.
"""


class RepositorioDeReservas:
    def ocupada(self, cancha, fecha, hora):
        """True si la cancha ya tiene una reserva a esa hora ese dia."""
        raise NotImplementedError

    def contar_del_estudiante(self, estudiante, fecha):
        """Cuantas reservas tiene el estudiante ese dia."""
        raise NotImplementedError

    def guardar(self, estudiante, cancha, fecha, hora):
        """Guarda una reserva nueva y la devuelve como Reserva, con su id."""
        raise NotImplementedError
