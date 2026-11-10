from adaptadores import ApiHttp, RepositorioEnMemoria, RepositorioSqlite
from casos_de_uso import ReservarCancha
from dominio import motivo_de_rechazo
from http_simulado import Solicitud
from reservas_acopladas import SOLICITUDES_DE_PRUEBA, ApiDeReservasAcoplada


def modulos_que_importa(archivo):
    """Los nombres de los modulos que importa un archivo de esta carpeta."""
    nombres = []
    with open(archivo, encoding="utf-8") as fuente:
        for linea in fuente:
            partes = linea.split()
            if len(partes) >= 2 and (partes[0] == "import" or partes[0] == "from"):
                nombres.append(partes[1].split(".")[0])
    return nombres


def test_las_reglas_se_prueban_sin_base_de_datos():
    assert motivo_de_rechazo("cancha-1", 18, False, 0) is None
    assert motivo_de_rechazo("cancha-9", 18, False, 0) == "cancha desconocida"
    assert motivo_de_rechazo("cancha-1", 22, False, 0) == "fuera del horario"
    assert motivo_de_rechazo("cancha-1", 18, True, 0) == "hora ocupada"
    assert motivo_de_rechazo("cancha-1", 18, False, 2) == "limite diario alcanzado"


def test_el_orden_de_las_reglas_es_el_mismo():
    assert motivo_de_rechazo("cancha-9", 22, True, 2) == "cancha desconocida"
    assert motivo_de_rechazo("cancha-1", 22, True, 2) == "fuera del horario"
    assert motivo_de_rechazo("cancha-1", 18, True, 2) == "hora ocupada"


def test_el_caso_de_uso_confirma_y_guarda_en_memoria():
    repositorio = RepositorioEnMemoria()
    resultado = ReservarCancha(repositorio).ejecutar("ana", "cancha-1", "2026-11-10", 18)
    assert resultado["estado"] == "confirmada"
    assert resultado["reserva"].id == "r-1"
    assert repositorio.ocupada("cancha-1", "2026-11-10", 18)
    assert repositorio.contar_del_estudiante("ana", "2026-11-10") == 1


def test_el_caso_de_uso_rechaza_sin_guardar():
    repositorio = RepositorioEnMemoria()
    caso = ReservarCancha(repositorio)
    caso.ejecutar("ana", "cancha-1", "2026-11-10", 18)
    resultado = caso.ejecutar("beto", "cancha-1", "2026-11-10", 18)
    assert resultado == {"estado": "rechazada", "motivo": "hora ocupada"}
    assert repositorio.contar_del_estudiante("beto", "2026-11-10") == 0


def test_el_limite_diario_cuenta_por_estudiante_y_por_dia():
    caso = ReservarCancha(RepositorioEnMemoria())
    caso.ejecutar("ana", "cancha-1", "2026-11-10", 8)
    caso.ejecutar("ana", "cancha-1", "2026-11-10", 9)
    assert caso.ejecutar("ana", "cancha-1", "2026-11-10", 10)["motivo"] == "limite diario alcanzado"
    assert caso.ejecutar("ana", "cancha-1", "2026-11-11", 10)["estado"] == "confirmada"
    assert caso.ejecutar("beto", "cancha-1", "2026-11-10", 10)["estado"] == "confirmada"


def test_por_capas_responde_igual_que_la_version_acoplada():
    acoplada = ApiDeReservasAcoplada(":memory:")
    por_capas = ApiHttp(ReservarCancha(RepositorioSqlite(":memory:")))
    for cuerpo in SOLICITUDES_DE_PRUEBA:
        antes = acoplada.manejar(Solicitud("POST", "/v1/reservas", cuerpo))
        despues = por_capas.manejar(Solicitud("POST", "/v1/reservas", cuerpo))
        assert (despues.estado, despues.cuerpo) == (antes.estado, antes.cuerpo)


def test_con_el_repositorio_en_memoria_la_api_responde_igual():
    acoplada = ApiDeReservasAcoplada(":memory:")
    en_memoria = ApiHttp(ReservarCancha(RepositorioEnMemoria()))
    for cuerpo in SOLICITUDES_DE_PRUEBA:
        antes = acoplada.manejar(Solicitud("POST", "/v1/reservas", cuerpo))
        despues = en_memoria.manejar(Solicitud("POST", "/v1/reservas", cuerpo))
        assert (despues.estado, despues.cuerpo) == (antes.estado, antes.cuerpo)


def test_el_dominio_no_importa_nada():
    assert modulos_que_importa("dominio.py") == []


def test_el_caso_de_uso_no_conoce_sqlite_ni_http():
    importados = modulos_que_importa("casos_de_uso.py")
    assert "sqlite3" not in importados
    assert "http_simulado" not in importados
    assert "adaptadores" not in importados
