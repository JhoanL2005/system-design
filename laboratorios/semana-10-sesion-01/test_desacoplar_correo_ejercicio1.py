from cola import ColaDeMensajes
from servicios import RepositorioDeReservas, ServicioDeCorreo
from desacoplar_correo_ejercicio1 import ServicioSincrono, ServicioConCola, TrabajadorDeCorreo


def test_sincrono_registra_la_reserva_y_aun_asi_responde_error():
    repositorio = RepositorioDeReservas()
    correo = ServicioDeCorreo()
    correo.caido = True
    servicio = ServicioSincrono(repositorio, correo)
    assert servicio.reservar("ana", "Cancha 1", 18) == "error"
    assert len(repositorio.reservas) == 1
    assert servicio.reservar("ana", "Cancha 1", 18) == "ocupada"


def test_con_cola_confirma_aunque_el_correo_este_caido():
    repositorio = RepositorioDeReservas()
    cola = ColaDeMensajes("correos")
    servicio = ServicioConCola(repositorio, cola)
    assert servicio.reservar("ana", "Cancha 1", 18) == "confirmada"
    assert len(repositorio.reservas) == 1
    assert cola.cantidad_disponibles() == 1


def test_con_cola_una_hora_ocupada_no_publica_nada():
    repositorio = RepositorioDeReservas()
    cola = ColaDeMensajes("correos")
    servicio = ServicioConCola(repositorio, cola)
    servicio.reservar("ana", "Cancha 1", 18)
    assert servicio.reservar("beto", "Cancha 1", 18) == "ocupada"
    assert cola.cantidad_disponibles() == 1


def test_el_trabajador_envia_y_confirma_cuando_el_correo_vuelve():
    repositorio = RepositorioDeReservas()
    correo = ServicioDeCorreo()
    correo.caido = True
    cola = ColaDeMensajes("correos")
    ServicioConCola(repositorio, cola).reservar("ana", "Cancha 1", 18)
    correo.caido = False
    TrabajadorDeCorreo(cola, correo).procesar_pendientes()
    assert correo.enviados == [("ana", "Reserva confirmada: Cancha 1 a las 18")]
    assert cola.cantidad_disponibles() == 0
    assert cola.cantidad_en_proceso() == 0
