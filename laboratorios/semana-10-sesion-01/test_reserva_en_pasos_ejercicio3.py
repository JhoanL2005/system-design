from cola import ColaDeMensajes
from servicios import RepositorioDeReservas
from infraestructura import AlmacenCompartido, BalanceadorRoundRobin
from reserva_en_pasos_ejercicio3 import ServidorConEstado, ServidorSinEstado


def test_con_estado_se_pierde_el_borrador_detras_del_balanceador():
    repositorio = RepositorioDeReservas()
    cola = ColaDeMensajes("correos")
    balanceador = BalanceadorRoundRobin([
        ServidorConEstado("A", repositorio, cola),
        ServidorConEstado("B", repositorio, cola),
    ])
    assert balanceador.siguiente().iniciar("ana", "Cancha 1") == "ok"
    assert balanceador.siguiente().elegir_hora("ana", 18) == "sin borrador"


def armar_sin_estado(cantidad):
    repositorio = RepositorioDeReservas()
    cola = ColaDeMensajes("correos")
    almacen = AlmacenCompartido()
    servidores = []
    for numero in range(cantidad):
        servidores.append(ServidorSinEstado("S" + str(numero), repositorio, cola, almacen))
    return repositorio, cola, almacen, BalanceadorRoundRobin(servidores)


def test_sin_estado_completa_la_reserva_en_servidores_distintos():
    repositorio, cola, almacen, balanceador = armar_sin_estado(2)
    assert balanceador.siguiente().iniciar("ana", "Cancha 1") == "ok"
    assert balanceador.siguiente().elegir_hora("ana", 18) == "ok"
    assert balanceador.siguiente().confirmar("ana") == "confirmada"
    assert repositorio.reservas == [{"estudiante": "ana", "cancha": "Cancha 1", "hora": 18}]
    assert cola.cantidad_disponibles() == 1


def test_elegir_hora_queda_guardada_en_el_almacen():
    repositorio, cola, almacen, balanceador = armar_sin_estado(2)
    balanceador.siguiente().iniciar("ana", "Cancha 1")
    balanceador.siguiente().elegir_hora("ana", 18)
    assert almacen.leer("borrador:ana") == {"cancha": "Cancha 1", "hora": 18}


def test_confirmar_borra_el_borrador():
    repositorio, cola, almacen, balanceador = armar_sin_estado(2)
    balanceador.siguiente().iniciar("ana", "Cancha 1")
    balanceador.siguiente().elegir_hora("ana", 18)
    balanceador.siguiente().confirmar("ana")
    assert almacen.leer("borrador:ana") is None
    assert balanceador.siguiente().confirmar("ana") == "sin borrador"


def test_sobrevive_a_que_un_servidor_se_reinicie_a_mitad():
    repositorio, cola, almacen, balanceador = armar_sin_estado(2)
    balanceador.siguiente().iniciar("ana", "Cancha 1")
    balanceador.reemplazar(0, ServidorSinEstado("S0-nuevo", repositorio, cola, almacen))
    balanceador.reemplazar(1, ServidorSinEstado("S1-nuevo", repositorio, cola, almacen))
    assert balanceador.siguiente().elegir_hora("ana", 18) == "ok"
    assert balanceador.siguiente().confirmar("ana") == "confirmada"


def test_agregar_un_servidor_a_mitad_no_rompe_nada():
    repositorio, cola, almacen, balanceador = armar_sin_estado(1)
    balanceador.siguiente().iniciar("ana", "Cancha 1")
    balanceador.agregar(ServidorSinEstado("S-extra", repositorio, cola, almacen))
    servidor = balanceador.siguiente()
    assert servidor.nombre == "S-extra"
    assert servidor.elegir_hora("ana", 18) == "ok"
    assert balanceador.siguiente().confirmar("ana") == "confirmada"


def test_sin_borrador_y_hora_ocupada():
    repositorio, cola, almacen, balanceador = armar_sin_estado(2)
    assert balanceador.siguiente().elegir_hora("beto", 18) == "sin borrador"
    balanceador.siguiente().iniciar("ana", "Cancha 1")
    balanceador.siguiente().iniciar("beto", "Cancha 1")
    balanceador.siguiente().elegir_hora("ana", 18)
    balanceador.siguiente().elegir_hora("beto", 18)
    assert balanceador.siguiente().confirmar("ana") == "confirmada"
    assert balanceador.siguiente().confirmar("beto") == "ocupada"
    assert len(repositorio.reservas) == 1
    assert cola.cantidad_disponibles() == 1
