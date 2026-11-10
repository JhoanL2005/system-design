from espera_ejercicio1 import CalendarioObservable, ListaDeEspera, ObservadorDeCalendario, simular_consultas
from notificaciones import NotificadorEnMemoria
from reservas import FranjaHoraria

DIECIOCHO = FranjaHoraria("2026-11-10", 18, 19)


class Anotador(ObservadorDeCalendario):
    def __init__(self, nombre, registro):
        self.nombre = nombre
        self.registro = registro

    def al_liberarse(self, cancha, franja):
        self.registro.append((self.nombre, cancha, franja))


def armar():
    notificador = NotificadorEnMemoria()
    lista = ListaDeEspera(notificador)
    calendario = CalendarioObservable("cancha-1", "2026-11-10")
    calendario.suscribir(lista)
    calendario.reservar("r-1", "ana", 18, 19)
    return calendario, lista, notificador


def test_consultar_cuesta_una_consulta_por_intervalo():
    assert simular_consultas(30) == (185, 5520)
    assert simular_consultas(300) == (20, 5700)


def test_cancelar_avisa_a_cada_observador_en_orden():
    registro = []
    calendario = CalendarioObservable("cancha-1", "2026-11-10")
    calendario.suscribir(Anotador("primero", registro))
    calendario.suscribir(Anotador("segundo", registro))
    calendario.reservar("r-1", "ana", 18, 19)
    calendario.cancelar("r-1")
    assert registro == [("primero", "cancha-1", DIECIOCHO), ("segundo", "cancha-1", DIECIOCHO)]


def test_el_aviso_llega_despues_de_cancelar():
    estados = []

    class MiraElCalendario(ObservadorDeCalendario):
        def al_liberarse(self, cancha, franja):
            estados.append(calendario.esta_libre(franja.inicio, franja.fin))

    calendario = CalendarioObservable("cancha-1", "2026-11-10")
    calendario.suscribir(MiraElCalendario())
    calendario.reservar("r-1", "ana", 18, 19)
    calendario.cancelar("r-1")
    assert estados == [True]


def test_reservar_no_avisa():
    registro = []
    calendario = CalendarioObservable("cancha-1", "2026-11-10")
    calendario.suscribir(Anotador("unico", registro))
    calendario.reservar("r-1", "ana", 18, 19)
    assert registro == []


def test_la_lista_avisa_al_primero_que_espera_esa_franja():
    calendario, lista, notificador = armar()
    lista.anotar("beto", DIECIOCHO)
    lista.anotar("dani", DIECIOCHO)
    calendario.cancelar("r-1")
    assert notificador.enviados == [("beto", "Se libero cancha-1 el 2026-11-10 de 18 a 19")]
    assert lista.esperando[DIECIOCHO] == ["dani"]


def test_una_franja_que_nadie_espera_no_avisa():
    calendario, lista, notificador = armar()
    calendario.reservar("r-2", "carla", 9, 10)
    lista.anotar("beto", DIECIOCHO)
    calendario.cancelar("r-2")
    assert notificador.enviados == []
    assert lista.esperando[DIECIOCHO] == ["beto"]
