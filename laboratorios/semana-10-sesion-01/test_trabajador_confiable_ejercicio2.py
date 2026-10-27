from cola import ColaDeMensajes
from servicios import ServicioDeCorreo
from trabajador_confiable_ejercicio2 import TrabajadorConfiable

CONFIRMACION = {"estudiante": "ana", "cancha": "Cancha 1", "hora": 18}


def armar(max_intentos=3):
    cola = ColaDeMensajes("correos")
    muertos = ColaDeMensajes("correos-muertos")
    correo = ServicioDeCorreo()
    trabajador = TrabajadorConfiable(cola, correo, muertos, max_intentos)
    return cola, muertos, correo, trabajador


def test_sin_mensajes_devuelve_false():
    cola, muertos, correo, trabajador = armar()
    assert trabajador.procesar_uno() is False


def test_confirma_despues_de_enviar():
    cola, muertos, correo, trabajador = armar()
    cola.publicar(CONFIRMACION)
    assert trabajador.procesar_uno() is True
    assert len(correo.enviados) == 1
    assert cola.cantidad_disponibles() == 0
    assert cola.cantidad_en_proceso() == 0


def test_si_un_trabajador_cae_a_mitad_el_mensaje_no_se_pierde():
    cola, muertos, correo, trabajador = armar()
    cola.publicar(CONFIRMACION)
    cola.recibir()
    assert trabajador.procesar_uno() is False
    cola.vencer_visibilidad()
    assert trabajador.procesar_uno() is True
    assert len(correo.enviados) == 1


def test_un_fallo_del_correo_deja_el_mensaje_para_otro_intento():
    cola, muertos, correo, trabajador = armar()
    cola.publicar(CONFIRMACION)
    correo.caido = True
    trabajador.procesar_uno()
    assert cola.cantidad_en_proceso() == 1
    correo.caido = False
    cola.vencer_visibilidad()
    trabajador.procesar_uno()
    assert len(correo.enviados) == 1
    assert cola.cantidad_en_proceso() == 0


def test_despues_de_max_intentos_va_a_la_cola_de_muertos():
    cola, muertos, correo, trabajador = armar(max_intentos=3)
    cola.publicar(CONFIRMACION)
    correo.caido = True
    for _ in range(3):
        trabajador.procesar_uno()
        cola.vencer_visibilidad()
    assert muertos.cantidad_disponibles() == 1
    assert cola.cantidad_disponibles() == 0
    assert cola.cantidad_en_proceso() == 0
    assert muertos.recibir()["cuerpo"] == CONFIRMACION


def test_un_mensaje_muerto_no_vuelve_a_la_cola():
    cola, muertos, correo, trabajador = armar(max_intentos=1)
    cola.publicar(CONFIRMACION)
    correo.caido = True
    trabajador.procesar_uno()
    cola.vencer_visibilidad()
    assert trabajador.procesar_uno() is False


def test_al_menos_una_vez_puede_entregar_dos_veces():
    cola, muertos, correo, trabajador = armar()
    cola.publicar(CONFIRMACION)
    cola.recibir()
    correo.enviar("ana", "Reserva confirmada: Cancha 1 a las 18")
    cola.vencer_visibilidad()
    trabajador.procesar_uno()
    assert len(correo.enviados) == 2
