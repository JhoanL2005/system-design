"""Ejercicio 1: el calendario en vivo de una cancha.

Cada app abierta en el calendario de una cancha tiene una conexion con el
servidor (conexiones.py). Cuando alguien reserva o cancela, todas las
apps que miran ese calendario tienen que verlo sin refrescar.

- Canales es el intermediario de publicador-suscriptor: cada tema (por
  ejemplo "cancha-1/2026-11-10") tiene su lista de conexiones suscritas.
  Quien publica en un tema no sabe quien lo escucha.
- PublicadorDeDisponibilidad es un observador del calendario de la Semana
  12 que, en cada cambio, publica un mensaje en el tema de ese calendario.

Corre el archivo con:

    python3 canales_ejercicio1.py

y las pruebas con:

    pytest test_canales_ejercicio1.py
"""

from calendario_eventos import CalendarioConEventos, ObservadorDeReservas
from conexiones import ConexionSimulada


def tema_de(cancha, fecha):
    return cancha + "/" + fecha


class Canales:
    def __init__(self):
        self.suscritos = {}

    def suscribir(self, tema, conexion):
        # TODO 1: agrega la conexion a la lista del tema (creala si no
        # existe). Si ya estaba suscrita a ese tema, no la agregues otra
        # vez. Escribe tambien desuscribir(tema, conexion), que la quita
        # si esta.
        raise NotImplementedError

    def suscriptores(self, tema):
        return len(self.suscritos.get(tema, []))

    def publicar(self, tema, mensaje):
        # TODO 2: envia el mensaje a cada conexion suscrita al tema y devuelve
        # cuantas lo recibieron (enviar devuelve True o False). Un tema
        # sin suscriptores devuelve 0.
        raise NotImplementedError


class PublicadorDeDisponibilidad(ObservadorDeReservas):
    def __init__(self, canales, fecha):
        self.canales = canales
        self.fecha = fecha
        self.ultimos_entregados = 0

    # TODO 3: al_ocuparse publica "ocupada 18-19" en el tema de esa cancha y
    # fecha (tema_de), y al_liberarse publica "libre 18-19", con las horas
    # de la franja. Guarda en self.ultimos_entregados lo que devolvio
    # publicar.


if __name__ == "__main__":
    fecha = "2026-11-10"
    canales = Canales()
    publicador = PublicadorDeDisponibilidad(canales, fecha)
    cancha_1 = CalendarioConEventos("cancha-1", fecha)
    cancha_2 = CalendarioConEventos("cancha-2", fecha)
    for calendario in [cancha_1, cancha_2]:
        calendario.suscribir("ocupada", publicador)
        calendario.suscribir("liberada", publicador)

    mirando_1 = []
    for i in range(300):
        conexion = ConexionSimulada("estudiante-" + str(i))
        canales.suscribir(tema_de("cancha-1", fecha), conexion)
        mirando_1.append(conexion)
    for i in range(50):
        canales.suscribir(tema_de("cancha-2", fecha), ConexionSimulada("visitante-" + str(i)))

    print("Mirando cancha-1:", canales.suscriptores(tema_de("cancha-1", fecha)))
    print("Mirando cancha-2:", canales.suscriptores(tema_de("cancha-2", fecha)))

    cancha_1.reservar("r-1", "ana", 18, 19)
    print("Mensajes al reservar cancha-1:", publicador.ultimos_entregados)
    print("Lo que recibio estudiante-0:", mirando_1[0].recibidos)

    canales.desuscribir(tema_de("cancha-1", fecha), mirando_1[0])
    canales.suscribir(tema_de("cancha-2", fecha), mirando_1[0])
    cancha_2.reservar("r-2", "beto", 9, 10)
    print("Mensajes al reservar cancha-2:", publicador.ultimos_entregados)

    mirando_1[1].cerrar()
    cancha_1.cancelar("r-1")
    print("Mensajes al cancelar cancha-1:", publicador.ultimos_entregados)
    print("Siguen suscritas a cancha-1:", canales.suscriptores(tema_de("cancha-1", fecha)))
    print("Lo que recibio estudiante-0:", mirando_1[0].recibidos)
