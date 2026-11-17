"""Ejercicio 2: las pruebas de contrato del repositorio.

El servicio se prueba rapido con RepositorioEnMemoria, un doble de prueba.
Eso solo vale si el doble se comporta igual que RepositorioSQLite. Estas
pruebas corren dos veces cada una, una con cada repositorio (la fixture
`repositorio` tiene dos parametros): si una pasa con uno y falla con el
otro, el doble miente.

    pytest test_contrato_repositorio_ejercicio2.py -v
"""

import sqlite3

import pytest

from dominio import semana_de
from repositorio import RepositorioEnMemoria, RepositorioSQLite


@pytest.fixture(params=["memoria", "sqlite"])
def repositorio(request, tmp_path):
    if request.param == "memoria":
        repo = RepositorioEnMemoria()
    else:
        repo = RepositorioSQLite(str(tmp_path / "reservau.db"))
    yield repo
    repo.cerrar()


def test_guardar_y_buscar(repositorio):
    repositorio.guardar("r1", "ana", "2026-11-17")
    assert repositorio.buscar("r1") == ("ana", "2026-11-17")


# TODO 1: buscar una reserva que no existe devuelve None.

# TODO 2: contar_en_semana cuenta solo las del estudiante en esa semana:
# guarda dos de ana en la semana del 16 de noviembre, una de ana en la del
# 23 y una de beto en la del 16, y comprueba los tres conteos.

# TODO 3: guardar dos veces el mismo id lanza sqlite3.IntegrityError
# (con pytest.raises).

# TODO 4: puntos_de suma todos los puntos del estudiante (0 si no tiene).
