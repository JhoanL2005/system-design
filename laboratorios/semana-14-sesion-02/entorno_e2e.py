"""El entorno de pruebas de punta a punta, simulado. No lo modifiques.

NavegadorSimulado arma ReservaU completo (API, servicio y una base SQLite
en un archivo nuevo) y lo usa como lo usaria una persona desde el
navegador: inicia sesion, llena formularios y aprieta botones. Para
parecerse a una prueba de punta a punta de verdad, cada accion tarda (el
navegador carga la pagina) y, de vez en cuando, falla por razones que no
tienen que ver con ReservaU (la red, el navegador, un servicio vecino).
"""

import os
import random
import tempfile
import time

from api import ApiDeReservas
from repositorio import RepositorioSQLite
from servicio import ServicioDeReservas

SEGUNDOS_POR_ACCION = 0.2
SEGUNDOS_POR_INICIO_DE_SESION = 0.4
PROBABILIDAD_DE_FALLA_AJENA = 0.01


class ErrorDelEntorno(Exception):
    """Una falla que no es de ReservaU: tiempo de espera agotado."""


class NavegadorSimulado:
    def __init__(self):
        carpeta = tempfile.mkdtemp()
        self.repositorio = RepositorioSQLite(os.path.join(carpeta, "reservau.db"))
        self.api = ApiDeReservas(ServicioDeReservas(self.repositorio))
        self.usuario = None

    def _esperar(self, segundos):
        time.sleep(segundos)
        if random.random() < PROBABILIDAD_DE_FALLA_AJENA:
            raise ErrorDelEntorno("tiempo de espera agotado esperando la pagina")

    def iniciar_sesion(self, usuario):
        self._esperar(SEGUNDOS_POR_INICIO_DE_SESION)
        self.usuario = usuario

    def reservar(self, id_reserva, fecha):
        self._esperar(SEGUNDOS_POR_ACCION)
        return self.api.manejar({"metodo": "POST", "ruta": "/reservas",
                                 "cuerpo": {"id": id_reserva, "estudiante": self.usuario, "fecha": fecha}})

    def cancelar(self, id_reserva, minutos_de_anticipacion):
        self._esperar(SEGUNDOS_POR_ACCION)
        return self.api.manejar({"metodo": "DELETE", "ruta": "/reservas/" + id_reserva,
                                 "cuerpo": {"minutos_de_anticipacion": minutos_de_anticipacion}})

    def ver_puntos(self):
        self._esperar(SEGUNDOS_POR_ACCION)
        return self.api.manejar({"metodo": "GET", "ruta": "/estudiantes/" + self.usuario + "/puntos"})["cuerpo"]["puntos"]
