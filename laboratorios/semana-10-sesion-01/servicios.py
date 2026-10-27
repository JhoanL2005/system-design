"""Los servicios con los que habla ReservaU. Ya estan completos: no los
modifiques.

RepositorioDeReservas guarda las reservas confirmadas (en un sistema
real, la base de datos). ServicioDeCorreo simula el proveedor de correo:
mientras esta caido, enviar(...) devuelve False y no envia nada.
"""


class RepositorioDeReservas:
    def __init__(self):
        self.reservas = []

    def esta_libre(self, cancha, hora):
        for reserva in self.reservas:
            if reserva["cancha"] == cancha and reserva["hora"] == hora:
                return False
        return True

    def registrar(self, estudiante, cancha, hora):
        self.reservas.append({"estudiante": estudiante, "cancha": cancha, "hora": hora})


class ServicioDeCorreo:
    def __init__(self):
        self.caido = False
        self.enviados = []

    def enviar(self, destinatario, asunto):
        if self.caido:
            return False
        self.enviados.append((destinatario, asunto))
        return True


def asunto_de_confirmacion(cuerpo):
    return "Reserva confirmada: " + cuerpo["cancha"] + " a las " + str(cuerpo["hora"])
