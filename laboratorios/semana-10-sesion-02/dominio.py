"""El almacenamiento de ReservaU y la pasarela de pagos. Ya estan
completos: no los modifiques.

RepositorioDeReservas guarda cada reserva como un diccionario con id,
estudiante, cancha, fecha y hora (un entero, de 7 a 20). Esa es la forma
interna del dato, la que conoce la base de datos: lo que ve un cliente
de la API lo decide cada version de la API.

PasarelaDePagos simula el proveedor que cobra la garantia de una reserva
a la tarjeta del estudiante. Cada llamada a cobrar(...) es un cobro de
verdad, y queda registrada en la lista cobros.
"""

CANCHAS = ["cancha-1", "cancha-2", "cancha-3"]
HORAS_DEL_DIA = [7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]


class RepositorioDeReservas:
    def __init__(self):
        self.reservas = {}
        self.siguiente_numero = 1

    def ocupada(self, cancha, fecha, hora):
        for reserva in self.reservas.values():
            if reserva["cancha"] == cancha and reserva["fecha"] == fecha and reserva["hora"] == hora:
                return True
        return False

    def libres(self, cancha, fecha):
        libres = []
        for hora in HORAS_DEL_DIA:
            if not self.ocupada(cancha, fecha, hora):
                libres.append(hora)
        return libres

    def crear(self, estudiante, cancha, fecha, hora):
        id_reserva = "r-" + str(self.siguiente_numero)
        self.siguiente_numero = self.siguiente_numero + 1
        self.reservas[id_reserva] = {
            "id": id_reserva,
            "estudiante": estudiante,
            "cancha": cancha,
            "fecha": fecha,
            "hora": hora,
        }
        return dict(self.reservas[id_reserva])

    def buscar(self, id_reserva):
        reserva = self.reservas.get(id_reserva)
        if reserva is None:
            return None
        return dict(reserva)

    def borrar(self, id_reserva):
        self.reservas.pop(id_reserva, None)


class PasarelaDePagos:
    def __init__(self):
        self.cobros = []

    def cobrar(self, estudiante, monto):
        id_cobro = "cobro-" + str(len(self.cobros) + 1)
        self.cobros.append({"id": id_cobro, "estudiante": estudiante, "monto": monto})
        return id_cobro
