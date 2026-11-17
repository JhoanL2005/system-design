from conexiones import ConexionSimulada
from servidores_ejercicio2 import BusEntreServidores, CanalesQueLimpian, ServidorDeConexiones

TEMA = "cancha-1/2026-11-10"
OTRO = "cancha-2/2026-11-10"


def test_las_conexiones_cerradas_se_quitan():
    canales = CanalesQueLimpian()
    a = ConexionSimulada("ana")
    b = ConexionSimulada("beto")
    canales.suscribir(TEMA, a)
    canales.suscribir(TEMA, b)
    a.cerrar()
    assert canales.publicar(TEMA, "hola") == 1
    assert canales.suscriptores(TEMA) == 1
    assert b.recibidos == ["hola"]


def test_todas_cerradas():
    canales = CanalesQueLimpian()
    for i in range(3):
        c = ConexionSimulada("x" + str(i))
        canales.suscribir(TEMA, c)
        c.cerrar()
    assert canales.publicar(TEMA, "hola") == 0
    assert canales.suscriptores(TEMA) == 0


def test_el_servidor_se_suscribe_al_bus_con_su_primera_conexion():
    bus = BusEntreServidores()
    servidor = ServidorDeConexiones("s1", bus)
    servidor.conectar(ConexionSimulada("ana"), TEMA)
    servidor.conectar(ConexionSimulada("beto"), TEMA)
    assert bus.servidores_por_tema[TEMA] == [servidor]


def test_el_bus_solo_envia_a_servidores_interesados():
    bus = BusEntreServidores()
    s1 = ServidorDeConexiones("s1", bus)
    s2 = ServidorDeConexiones("s2", bus)
    s1.conectar(ConexionSimulada("ana"), TEMA)
    s1.conectar(ConexionSimulada("beto"), TEMA)
    s2.conectar(ConexionSimulada("carla"), OTRO)
    assert bus.publicar(TEMA, "ocupada 18-19") == 2
    assert bus.envios == 1


def test_el_servidor_se_desuscribe_con_su_ultima_conexion():
    bus = BusEntreServidores()
    servidor = ServidorDeConexiones("s1", bus)
    a = ConexionSimulada("ana")
    b = ConexionSimulada("beto")
    servidor.conectar(a, TEMA)
    servidor.conectar(b, TEMA)
    servidor.desconectar(a, TEMA)
    assert bus.servidores_por_tema[TEMA] == [servidor]
    servidor.desconectar(b, TEMA)
    assert bus.servidores_por_tema[TEMA] == []
    assert bus.publicar(TEMA, "hola") == 0
    assert bus.envios == 0


def test_un_servidor_que_pierde_todas_sus_conexiones_no_salta_al_siguiente():
    bus = BusEntreServidores()
    s1 = ServidorDeConexiones("s1", bus)
    s2 = ServidorDeConexiones("s2", bus)
    cerrada = ConexionSimulada("ana")
    abierta = ConexionSimulada("beto")
    s1.conectar(cerrada, TEMA)
    s2.conectar(abierta, TEMA)
    cerrada.cerrar()
    assert bus.publicar(TEMA, "hola") == 1
    assert abierta.recibidos == ["hola"]
    assert bus.servidores_por_tema[TEMA] == [s2]
